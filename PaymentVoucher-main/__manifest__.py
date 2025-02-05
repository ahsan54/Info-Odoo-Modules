{
    'name': 'Bss Payment Voucher',  # Module name
    'author': 'Ahsan Ismail',  # Author name
    'maintainer': 'M.Rizwan',  # Author name
    'description': "This is BSS Payment Voucher Module",  # Description about the app
    'version': '17.0.1.0',  # Correct version format for Odoo 17
    'summary': 'Payment Voucher: create Journal entry with debit lines only',  # Brief info about the app
    'sequence': 2,  # Position in the apps menu
    'category': 'BSS',  # Category displayed in info
    'website': 'https://www.bssuniversal.com',  # Website displayed in info
    'depends': ['base', 'account', 'account_accountant'],  # Dependencies
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/payment_voucher_view.xml',
        'views/account_move_inherited_view.xml',
    ],

}
