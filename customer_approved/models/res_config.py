
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_approve_customers = fields.Boolean('Auto Approve Customers',default=False)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        config_parameters = self.env["ir.config_parameter"].sudo()
        for record in self:
            config_parameters.sudo().set_param("customer_approved.auto_approve_customers",
                                               record.auto_approve_customers)
    def get_values(self):
        res = super(ResConfigSettings,self).get_values()
        config_parameters = self.env["ir.config_parameter"].sudo()
        res.update(
            auto_approve_customers=config_parameters.sudo().get_param(
                "customer_approved.auto_approve_customers", default=False),
        )
        return res