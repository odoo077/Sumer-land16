{
    "name": "Purchase Auto Landed Cost Creation",
    "summary": """
        Purchase Auto Landed Cost Creation
    """,
    "description": """
        Create landed costs directly from purchase order.
    """,
    "author": "Sanesquare Private Limited",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "AGPL-3",
    "category": "Uncategorized",
    "version": "16.0.1.0.1",
    "images": ["static/description/app_image.png"],
    "depends": ["base", "stock", "purchase", "stock_landed_costs"],
    "data": [
        "views/purchase_views.xml",
        "views/stock_landed_cost_views.xml",
        "views/land_cost.xml",
        "security/ir.model.access.csv",
    ],
}
