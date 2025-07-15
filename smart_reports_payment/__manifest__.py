{
    'name': "Smart Reports Payment",

    'summary': """
        Smart Reports Payment """,

    'description': """Smart Reports Payment""",
    'author': 'RASHAD ALKHAWLANI - SMART BUSINESS TECH ',
    'website': 'https://www.smart-bt.com',
    'category': 'Accounting',
    'version': '15.0.0.0',
    'depends': ['account'],
    'qweb': [],
    'data': ['views/main_inherit.xml',
             # 'views/styleslink.xml',
             'views/report_payment_receipt_modern.xml',
    ],
    "assets": {
        "web.report_assets_common": [
            'smart_reports_payment/static/src/scss/almaraifont.scss',
            'smart_reports_payment/static/src/scss/variables.scss',
            'smart_reports_payment/static/src/scss/invoice_style.scss',
        ],
    },
    'installable': True,
    'auto_install': False,
}