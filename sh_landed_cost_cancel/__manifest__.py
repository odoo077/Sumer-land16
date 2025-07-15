# -*- coding: utf-8 -*-
{
    "name": "Cancel Landed Costs",
    "author": "Technologies",
    "category": "Extra Tools",
    "license": "OPL-1",
    "version": "15.0.4",
    "depends": [

              "purchase", "sale_management", "stock", "stock_landed_costs"
    ],
    "application": True,
    "data": [
        'security/landed_cost_security.xml',
        'data/data.xml',
        'views/stock_config_settings.xml',
        'views/views.xml',
    ],

    "auto_install": False,
    "installable": True,
}
