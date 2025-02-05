from self import self

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


class BigLoan(models.Model):
    _name = 'big.loan'
    _description = 'Big Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'reference_number'

    employee_id = fields.Many2one('hr.employee', 'Employee')
    loan_type_id = fields.Many2one('big.loan.type', 'Loan Type')

    reference_number = fields.Char(readonly=True, copy=False, default=lambda self: _('New'))
    applied_date = fields.Date('Applied Date')
    approved_date = fields.Date('Approved Date')
    department_id = fields.Char('Department', related='employee_id.department_id.name', store=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    state = fields.Selection([('draft', 'Draft'), ('hr_approved', 'HR Approved'), ('fin_approved', 'Finance Approved'),
                              ('rejected', 'Rejected')], 'Status', default='draft')

    currency_id = fields.Many2one('res.currency', 'Currency')
    loan_amount = fields.Monetary('Loan Amount')
    is_interest = fields.Boolean('Interest', related='loan_type_id.is_interest_payable', store=True)
    installments = fields.Integer('No.Installments', related='loan_type_id.no_of_installments', store=True)
    rate = fields.Float('Rate', related='loan_type_id.policy_rate', store=True)
    payment_start_day = fields.Datetime('Payment Start Day')
    interest_amount = fields.Float('Interest Amount')

    total_loan = fields.Float('Total Loan')
    received_from_employee = fields.Float('Received From Employee', compute='_compute_received_from_employee')
    remaining_amount = fields.Float('Remaining Amount', compute='_compute_received_from_employee')

    debit_account_id = fields.Many2one('account.account', 'Loan Account')
    credit_account_id = fields.Many2one('account.account', 'Treasure Account')
    related_journal_entry = fields.Many2one('account.move', 'Related Journal Entry')
    related_profit_journal_entry = fields.Many2one('account.move', 'Related Profit Journal Entry')

    loan_page_ids = fields.One2many('big.loan.page', 'big_loan_id', 'Page Ids')

    @api.depends('loan_page_ids.next_instalment_size', 'loan_page_ids.is_paid')
    def _compute_received_from_employee(self):
        for x in self:
            received = sum(loan.next_instalment_size for loan in x.loan_page_ids if loan.is_paid)
            print(received)

            x.received_from_employee = received
            x.remaining_amount = x.total_loan - received

    @api.onchange('loan_amount', 'rate')
    def _onchange_interest_amount(self):
        for x in self:
            if x.rate:
                x.interest_amount = x.loan_amount / 100 * x.rate
                x.total_loan = x.loan_amount + x.interest_amount
            else:
                x.interest_amount = 0
                x.total_loan = x.loan_amount

    def compute_installments(self):
        for x in self:
            start_date = x.applied_date + relativedelta(months=+1)
            x.update({'payment_start_day': start_date})

            if x.installments <= 0:
                raise UserError('Installments cannot be less than or equal to zero.')

            x.loan_page_ids.unlink()

            for i in range(x.installments):
                payment_dates = x.payment_start_day + relativedelta(months=i) if x.payment_start_day else False

                rec = self.env['big.loan.page'].create({
                    'big_loan_id': x.id,
                    'next_month_date': payment_dates,
                    'next_instalment_size': x.total_loan / x.installments,
                    'is_paid': False,
                    'principle_amount': x.loan_amount / x.installments,
                    'interest_amount': x.interest_amount / x.installments,
                })
                print(f'Created Loan Page Record ID: {rec.id}, Next Month Date: {rec.next_month_date}')

    @api.model
    def create(self, vals):
        if vals.get('reference_number', _('New')) == _('New'):
            vals['reference_number'] = self.env['ir.sequence'].next_by_code('big.loan') or _('New')
            print(f"Generated Reference No: {vals['reference_number']}")
        return super(BigLoan, self).create(vals)

    @api.constrains('employee_id')
    def ensure_one_employee_can_only_apply_more_than_one_loan_in_current_year(self):
        for loan in self:
            current_year = date.today().year

            existing_loans = self.env['big.loan'].search([
                ('employee_id', '=', loan.employee_id.id),
                ('id', '!=', loan.id),
            ])

            for existing_loan in existing_loans:
                if existing_loan.loan_page_ids:
                    last_installment_date = max(
                        page.next_month_date for page in existing_loan.loan_page_ids if page.next_month_date
                    )
                    one_year_after_last_installment = last_installment_date

                    if loan.applied_date and loan.applied_date < one_year_after_last_installment:
                        raise ValidationError(
                            f"Employee {loan.employee_id.name} already has an active loan "
                            f"and cannot apply for another loan within one year of the last installment."
                        )

    def button_cancel(self):
        for x in self:
            x.update({'state': 'rejected'})

    def button_hr_approval(self):
        for x in self:
            if not x.loan_page_ids:
                raise UserError('Please Compute Installments First')
            if x.total_loan == sum(loan.next_instalment_size for loan in x.loan_page_ids if loan.next_instalment_size):
                x.update({'state': 'hr_approved'})
            else:
                raise UserError('Please Recompute Installments')

        sc = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        if sc:
            sc.write({'play_id': x.reference_number})

    def button_finance_approval(self):
        for x in self:
            x.update({'state': 'fin_approved'})
            x.update({'approved_date': date.today()})

            data = []

            debit_lines = {
                'account_id': x.debit_account_id.id,
                'name': x.reference_number,
                'debit': x.loan_amount,
                'credit': 0.0,
                'tax_tag_ids': False
            }

            data.append((0, 0, debit_lines))

            credit_lines = {
                'account_id': x.credit_account_id.id,
                'name': x.reference_number,
                'debit': 0.0,
                'credit': x.loan_amount,
                'tax_tag_ids': False
            }
            data.append((0, 0, credit_lines))

            vals = {
                'line_ids': data,
                'invoice_date': x.approved_date,
                'move_type': 'entry',
                'journal_linking_id': x.id,
            }

            self.env['account.move'].create(vals)
            x.update({'related_journal_entry': self.env['account.move'].search([('journal_linking_id', '=', x.id)],
                                                                               limit=1).id})
            sc = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
            if sc:
                sc.write({'received_from_employee': x.received_from_employee})
                sc.write({'remaining_amount': x.remaining_amount})
                sc.write({'applied_date': x.applied_date})
                sc.write({'approved_date': x.approved_date})
                sc.write({'loan_type': x.loan_type_id.name})
                sc.write({'interest_rate': x.rate})
                sc.write({'principal_amnt': x.loan_amount})
                sc.write({'total_loan_amount': x.total_loan})

    ############---------------------------------------------------------------------------------------------------: Profit Jv
    ############---------------------------------------------------------------------------------------------------:
    def create_update_profit_journal_jv(self):
        for x in self:
            if x.state == 'fin_approved':
                data = []
                income_line_debit = {
                    'account_id': x.credit_account_id.id,
                    'name': False,
                    'debit': sum(page.interest_amount for page in x.loan_page_ids if page.is_paid),
                    'credit': 0.0,
                }
                data.append((0, 0, income_line_debit))

                income_line_credit = {
                    'account_id': self.env['account.account'].search([('name', '=', 'Loan Interest Profit')],
                                                                     limit=1).id,
                    'name': x.reference_number,
                    'debit': 0.0,
                    'credit': sum(page.interest_amount for page in x.loan_page_ids if page.is_paid),
                }
                data.append((0, 0, income_line_credit))

                existing_move = self.env['account.move'].search([
                    ('journal_profit_id', '=', self._origin.id),
                    ('journal_linking_id', '=', False),
                    ('move_type', '=', 'entry')
                ], limit=1)

                if existing_move:
                    print(f"Updating existing journal entry: {existing_move.id}")
                    existing_move.write({
                        'line_ids': [(5, 0, 0)] +  # Remove existing lines
                                    [(0, 0, income_line_debit), (0, 0, income_line_credit)],
                    })
                else:
                    # Create a new journal entry
                    vals = {
                        'line_ids': data,
                        'invoice_date': x.approved_date,
                        'move_type': 'entry',
                        'journal_profit_id': self._origin.id,
                        # onchnage and some others like this use origin_id for current id so use origin as simple id is not callable in these methods.
                    }
                    print('id: ', x.id)
                    self.env['account.move'].create(vals)
                    x.update(
                        {'related_profit_journal_entry': self.env['account.move'].search(
                            [('journal_profit_id', '=', x.id)],
                            limit=1).id})

    # Here I Call The Profit Jv Function in write so each time on clicking boolean filed it should call method ....
    @api.model
    def write(self, vals):
        result = super().write(vals)
        if 'loan_page_ids' in vals:
            self.create_update_profit_journal_jv()
        return result

    # related_journal_to_update = self.env['account.move.line'].search(
    #     [('name', '=', self.reference_number)]).filtered(
    #     lambda r: r.account_id.id == self.env['account.account'].search([('name', '=', 'Loan Interest Profit')],
    #                                                                     limit=1).id)
    # if related_journal_to_update:
    #     related_journal_to_update.write(
    #         {'credit': sum(page.interest_amount for page in x.loan_page_ids if page.is_paid)})
    #####--------------------------------------------------------------------------------------------------------- END OF PROFIT Jv
    #####--------------------------------------------------------------------------------------------------------- END OF PROFIT Jv

    #####---------------------------------------------------------------------: Start Of Button Box : Counts :---------------------------------------
    #####---------------------------------------------------------------------: Start Of Button Box : Counts
    #####---------------------------------------------------------------------: Start Of Button Box : Counts :---------------------------------------

    count_journal_entry = fields.Char(string='Journal Count', compute='_compute_profit_jv_and_journal_entry')
    count_profit_jv = fields.Char(string='Profit Journal Count', compute='_compute_profit_jv_and_journal_entry')

    def _compute_profit_jv_and_journal_entry(self):
        for x in self:
            count_journal = self.env['account.move'].search_count([
                ('journal_linking_id', '=', x.id)])
            x.count_journal_entry = count_journal

            count_profit = self.env['account.move'].search_count([
                ('journal_profit_id', '=', x.id)])
            x.count_profit_jv = count_profit

    def action_open_journal_tree_view(self):
        for x in self:
            return {
                'name': 'Journal Entry',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'domain': [('journal_linking_id', '=', x.id)],
                'context': {'create': False, 'delete': False},
                'type': 'ir.actions.act_window',
                'target': 'current',
            }

    def action_open_profit_jv_tree_view(self):
        for x in self:
            return {
                'name': 'Profit Journal',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'domain': [('journal_profit_id', '=', x.id)],
                'context': {'create': False, 'delete': False},
                'type': 'ir.actions.act_window',
                'target': 'current',
            }


class Page_Loan(models.Model):
    _name = 'big.loan.page'
    _description = 'Page Loan'

    big_loan_id = fields.Many2one('big.loan', 'Big Loan')

    next_instalment_size = fields.Float('Instalment Size')
    next_month_date = fields.Date('Date')
    is_paid = fields.Boolean('Paid')
    principle_amount = fields.Float('Principle Amount')
    interest_amount = fields.Float('Interest Amount')


class LinkingJournalEntry(models.Model):
    _inherit = 'account.move'

    journal_linking_id = fields.Many2one('big.loan', 'Simple Linking TO Loan')
    journal_profit_id = fields.Many2one('big.loan', 'Link To Related Loan')

