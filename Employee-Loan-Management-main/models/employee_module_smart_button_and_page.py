from odoo import models, fields, api, _
from datetime import date, datetime

from odoo.addons.mail.tests.common import mail_new_test_user


class EmployeeFormLoanPage(models.Model):
    _inherit = 'hr.employee'

    link_id = fields.Many2one('big.loan', string='Loan ID', compute='_compute_link')

    play_id = fields.Char(string='Play ID', readonly=True)

    applied_date = fields.Date(string='Applied Date')
    approved_date = fields.Date(string='Approved Date')
    loan_type = fields.Char(string='Loan Type')
    interest_rate = fields.Float(string='Interest Rate')
    principal_amnt = fields.Float(string='Principal Amount')
    total_loan_amount = fields.Float(string='Total Loan Amount')
    received_from_employee = fields.Float(string='Received From Employee')
    remaining_amount = fields.Float(string='Remaining Amount')



class HrEmployeeSmartButton(models.Model):
    _inherit = 'hr.employee'

    count_big_loans = fields.Char(string='Count of Loans', compute='_compute_big_loans')

    def _compute_big_loans(self):
        for x in self:
            sc = x.env['big.loan'].search([('employee_id', '=', x.id), ('state', 'in', ['hr_approved'])])
            x.count_big_loans = len(sc) + 1

    def action_open_employee_loan_tree_view(self):
        return {
            'name': f'Loans of {self.name}',
            'view_mode': 'tree,form',
            'res_model': 'big.loan',
            'domain': [('employee_id', '=', self.id)],
            'context': {'create': False, 'delete': False},
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
