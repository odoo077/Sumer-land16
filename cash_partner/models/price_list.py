from odoo import fields, models, api


class PriceList(models.Model):
    _inherit = "product.pricelist"
    journal_id = fields.Many2one("account.journal",domain="[('type','in',('bank','cash'))]")
