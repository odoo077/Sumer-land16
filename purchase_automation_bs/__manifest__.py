# -*- coding: utf-8 -*-
{
    'name': "Smart Purchase Automation",

    'summary': """
        Smart Purchase Automation""",

    'description': """
        Using this module User can create a PO and on confirm click the receipt and bill will create automatically
    """,

    'license': 'LGPL-3',
    'author': 'RASHAD ALKHAWLANI - SMART BUSINESS TECH ',
    'website': 'https://www.smart-bt.com',
    'category': 'Purchase',
    'version': '14.0.1.0.0',
    'depends': ['purchase', 'stock'],

    'data': [
        'views/setting.xml',
    ],
    'application': True,
    'installable': True,
}
