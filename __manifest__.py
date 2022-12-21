# -*- coding: utf-8 -*-
{
    'name': "product_bundle",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'assets': {

        'web.assets_frontend': [
            '/product_bundle/static/store_frontend_bundle.js',
            '/product_bundle/static/store_cart_bundle.js'
        ],
    },

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
     'depends': ['base', 'product','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/bundle.xml',
        'views/product.xml',
        'views/bundle_product_line.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
