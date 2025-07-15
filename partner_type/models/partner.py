from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection([
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail')], string="Customer Type",default='retail')

class PartnerUpdateTypeWizard(models.TransientModel):
    _name = "partner.update.type"
    _description = "Update the type for partners"

    partner_type = fields.Selection([
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail')], string="Customer Type")

    def update_partner_type(self):

        partners = self.env['res.partner'].browse(self._context.get('active_ids'))
        for partner in partners:
            partner.partner_type = self.partner_type
