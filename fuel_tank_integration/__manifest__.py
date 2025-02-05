# -*- coding: utf-8 -*-
{
    'name': "Fuel Tank Integration",

    'summary': """
        Fleet Fuel Consumption Tank management odoo apps is very useful for fuel management process, specially fleet management companies will require module""",

    'description': """
        Long description of module's purpose
    """,

    'author': "M.Rizwan",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '0.1',
    'sequence': -100,
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/add_fuel_wizard_view.xml',
        'views/fuel_tank_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
