from odoo import fields, models, api

class Product(models.Model):
    _inherit = "product.template"
    
    @api.onchange('property_account_expense_id','property_account_income_id','name')
    def _onchnage_property_account_income_id(self):
        if not self.name:
            self.property_account_expense_id=''
            self.property_account_income_id=''
            
class Payment(models.Model):
    _inherit = "account.payment"
    cost_id = fields.Many2one("purchase.landed.cost.line",copy=False)

    # def action_draft(self):
    #     res = super(Payment, self).action_post()
    #     for res in self:
    #         if res.cost_id:
    #             res.cost_id.payment_value -= res.amount
    #             if res.cost_id.payment_state:
    #                 res.cost_id.payment_state == False
    #     return res

    def action_post(self):
        res = super(Payment,self).action_post()
        for res in self:
            if res.cost_id:
                res.cost_id.payment_value+= res.amount
                if res.cost_id.payment_value==res.cost_id.amount:
                    res.cost_id.payment_state=True
        return res
