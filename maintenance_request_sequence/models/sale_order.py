from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    maintenance_request_id = fields.Many2one(
        'maintenance.request',
        string='Maintenance Request',
        help='Select the related Maintenance Request by its sequential number'
    )
