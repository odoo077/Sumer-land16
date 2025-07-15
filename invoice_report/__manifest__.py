{
    'name': 'Invoice Report',
    'version': '1.0',
    'category': '',
    'sequence': 14,
    'author': '',
    'company': '',
    'license': 'LGPL-3',
    'website': '',
    'summary': '',
    'depends': ['base', 'sale', 'account','product_updates'],
    'data': [

        # 'security/contact.xml',
        # 'security/ir.model.access.csv',
        'views/pdf_report.xml',
        'views/invoice.xml',

    ],
    'demo': [],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
