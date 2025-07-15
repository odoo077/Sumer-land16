# -*- coding: utf-8 -*-
{
    'name': "cash_partner",

    'summary': """
        cash customer  create saleorder and delivery and create invoice and payment """,

    'description': """
        Long description of module's purpose
    """,

    'author': "MOHAMED ABDELRHMAN",

    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
