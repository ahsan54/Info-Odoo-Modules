{
    'name': 'Big Loan',  # Module name
    'author': 'Muhammad Ahsin',  # Author name
    'description': "This is Loan",  # Description about the app
    'version': '17.0.1.0',  # Correct version format for Odoo 17
    'summary': 'Loan',  # Brief info about the app
    'sequence': 2,  # Position in the apps menu
    'category': 'Pakistan',  # Category displayed in info
    'website': 'https://www.google.com',  # Website displayed in info
    'depends': ['base', 'hr', 'account'],  # Dependencies
    'installable': True,
    'application': True,



    'data': [
        'security/ir.model.access.csv',
        'views/emp_loan_view.xml',
        'views/employee_module_smart_page_view.xml',
        'views/loan_types.xml'
    ],

}
