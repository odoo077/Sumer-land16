# -*- coding: utf-8 -*-
{
    "name": "Smart Auto Reconciliation",
    'version' : '15.0.1.0.0',
    'author': 'RASHAD ALKHAWLANI - SMART BUSINESS TECH ',
    'website': 'https://www.smart-bt.net',
    'depends': ['account'],
    'description': """
    Auto partial/full reconcile multiple invoice on payment
    """,
    "data": [
        'security/ir.model.access.csv',
        'views/account_payment_view.xml',
    ],
    'application': True,
    'installable': True,
    "license": "LGPL-3",
}
