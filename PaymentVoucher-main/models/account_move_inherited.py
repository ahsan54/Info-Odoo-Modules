from odoo import api,_,models,fields

class AccountMoveInherited(models.Model):
    _inherit = 'account.move'

    pv_id = fields.Many2one('payment.voucher','Payment Vouncher')
    cheque_no = fields.Char('Cheque#')

