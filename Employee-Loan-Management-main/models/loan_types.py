from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


class BigLoan(models.Model):
    _name = 'big.loan.type'
    _description = 'Big Loan Type'

    name = fields.Char('Loan Name')
    is_interest_payable = fields.Boolean('Is Interest Payable')
    policy_rate = fields.Float('Policy Rate')
    no_of_installments = fields.Integer('No. Of Installments')

    @api.constrains('name', 'policy_rate', 'is_interest_payable')
    def validate_type_related(self):
        for type in self:
            if not type.name:
                raise ValidationError('Name Of Loan Required...!')


