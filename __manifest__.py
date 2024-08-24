# -*- coding: utf-8 -*-
{
    'name': "material_note",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/templates_web_header.xml',
        'views/templates_web.xml',
        'views/templates_web_edit.xml',
        'views/templates_web_delete.xml',
        'views/templates_web_delete_modal.xml',
        'views/templates_web_new.xml',
        'views/templates_web_supplier.xml',
        'views/templates_web_edit_supplier.xml',
        'views/templates_web_delete_supplier.xml',
        'views/templates_web_new_supplier.xml',
        "views/material.xml",
        "views/supplier.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
        'demo/supplier.xml',
        'demo/om.suppliers.csv',
        'demo/om.materials.csv',
    ],

    'assets': {
        'web.assets_frontend': [
            'material_note/static/src/js/delete_confirmation.js',
        ],
    },

    'sequence': -100,
    'installable': True,
    'application': True,
    'auto_install': False,
}
