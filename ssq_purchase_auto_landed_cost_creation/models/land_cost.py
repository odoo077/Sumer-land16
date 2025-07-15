from odoo import fields, models, api


class LandCost(models.Model):
    _inherit = "stock.landed.cost.lines"
    partner_id = fields.Many2one("res.partner", string="الوكيل")


class LandCost(models.Model):
    _inherit = "stock.landed.cost"

    # def button_validate(self):
    #     res = super(LandCost, self).button_validate()
    #     if self.account_move_id:


class AdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    def _create_account_move_line(self, move, credit_account_id, debit_account_id, qty_out, already_out_account_id):
        res = super(AdjustmentLines,self)._create_account_move_line(move, credit_account_id, debit_account_id, qty_out, already_out_account_id)

        if self.cost_line_id.partner_id:
            for rec in res:
                dict1 = dict(rec[2])
                if dict1['account_id']:
                    account_id = self.env['account.account'].search([('id','=',dict1['account_id'])])
                    if account_id.user_type_id.type in ('receivable','payable'):
                        dict1['partner_id'] = self.cost_line_id.partner_id.id
                rec[2]=dict1
            # res['partner_id'] = self.cost_line_id.partner_id.id
        return res