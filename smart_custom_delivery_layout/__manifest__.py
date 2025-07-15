{
    'name': 'Custom Text on Delivery Report',
    'version': '15.0',
    'category': 'Delivery',
    'summery': 'Add custom text to delivery reports',
    'author': 'Khattab aldabagh - SMART BUSINESS TECH ',
    'website': "https://smart-bt.net/",
    'depends': ['stock'],
    
    'data': [
        'views/delivery_order_view.xml',
        'report/delivery_order_report.xml',
    ],
    
    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
