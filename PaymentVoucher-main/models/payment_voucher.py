from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


class PaymentVoucher(models.Model):
    _name = 'payment.voucher'
    _description = 'Payment Voucher'

    name = fields.Char(readonly=True, default=lambda self: _('New'))
    accounting_date = fields.Date('Date')
    cheque_no = fields.Char('Cheque#')
    journal_id = fields.Many2one('account.journal', string='Journal', domain=[('type', 'in', ['bank', 'cash'])])
    line_ids = fields.One2many('payment.voucher.line', 'payment_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
    ], default='draft')
    move_id = fields.Many2one('account.move', string='Journal Entry')
    journal_type = fields.Selection(related='journal_id.type', string='Journal Type')
    partner_id = fields.Many2one('res.partner', string='Partner')

    @api.model
    def create(self, vals):
        print(vals)
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('payment.voucher') or _('New')
        if vals.get('journal_id'):
            journal = self.env['account.journal'].search([('id', '=', vals['journal_id'])])
            print(journal.type)
            if journal.type == 'bank':
                vals['cheque_no'] = self.env['ir.sequence'].next_by_code('payment.voucher.cheque')
                vals['name'] = f'BPV{vals["name"]}'
            if journal.type == 'cash':
                vals['name'] = f'CPV{vals["name"]}'
        return super().create(vals)

    def button_confirm(self):
        data = []
        for line in self.line_ids:
            debit_line = {
                'account_id': line.account_id.id,
                'partner_id': self.partner_id.id,
                'name': line.narration,
                'debit': line.amount_debt,
                'credit': 0
            }
            data.append((0, 0, debit_line))
        credit_line = {
            'account_id': self.journal_id.default_account_id.id,
            'partner_id': self.partner_id.id,
            'name': '',
            'debit': 0,
            'credit': sum([line.amount_debt for line in self.line_ids])
        }
        data.append((0, 0, credit_line))
        vals = {
            'line_ids': data,
            'date': self.accounting_date,
            'journal_id': self.journal_id.id,
            'move_type': 'entry',
            'pv_id': self.id,
            'cheque_no': self.cheque_no,
        }
        print(vals)
        jv = self.env['account.move'].create(vals)
        self.move_id = jv.id
        if self.move_id:
            self.state = 'posted'
        self.action_view_jv()

    def action_view_jv(self):
        # To open Form view
        return {
            'type': 'ir.actions.act_window',
            'name': f'Journal Entry',
            'res_model': 'account.move',
            'view_mode': 'form',
            'context': {'create': False, 'delete': False},
            'res_id': self.move_id.id,
        }


        # To open in Tree
        # return {
        #     'name': f'Journal Entry',
        #     'view_mode': 'tree,form',
        #     'res_model': 'account.move',
        #     'domain': [('pv_id', '=', self.id)],
        #     'context': {'create': False, 'delete': False},
        #     'type': 'ir.actions.act_window',
        #     'target': 'current',
        # }


class PaymentVoucherLine(models.Model):
    _name = 'payment.voucher.line'

    account_id = fields.Many2one('account.account', 'Account')
    narration = fields.Char('Narration')
    amount_debt = fields.Float('Amount')
    payment_id = fields.Many2one('payment.voucher')


