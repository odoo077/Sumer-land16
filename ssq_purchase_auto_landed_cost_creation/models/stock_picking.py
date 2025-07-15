from odoo import fields, models
from datetime import datetime
import itertools

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if res == True and self.purchase_id.landed_cost_lines:
            line_data = []
            for line in self.env["purchase.landed.cost.line"].search(
                [("purchase_id", "=", self.purchase_id.id), ("is_landed_cost_created", "=", False)]
            ):
                line_data.append(
                    (
                        0,
                        0,
                        {
                            "product_id": line.product_id.id,
                            "name": line.name,
                            "account_id": line.account_id.id,
                            "split_method": line.split_method,
                            "price_unit": line.price_unit,
                            "partner_id":line.partner_id.id if line.partner_id else ''
                        },
                    )
                )
                line.is_landed_cost_created = True
            landed_cost = self.env["stock.landed.cost"].create(
                {
                    "date": datetime.now().date(),
                    "purchase_id": self.purchase_id.id,
                    "picking_ids": self.ids,
                    "cost_lines": line_data,
                }
            )
            self.sudo().purchase_id.landed_costs_ids = [(4, landed_cost.id)]
            landed_cost.sudo().with_context({"is_purchase_auto_calculation": True}).button_validate()
#             landed_cost.account_move_id.branch_id = self.purchase_id.branch_id.id if self.purchase_id.branch_id else''
#             if self.purchase_id.branch_id:
#                 for rec in landed_cost.account_move_id.line_ids:
#                     rec.branch_id=self.purchase_id.branch_id.id

        return res
    # def button_validate(self):
    #     res = super(StockPicking, self).button_validate()
    #     if res == True and self.purchase_id.landed_cost_lines:
    #         line_data = []
    #         for line in self.env["purchase.landed.cost.line"].search(
    #             [("purchase_id", "=", self.purchase_id.id), ("is_landed_cost_created", "=", False)]
    #         ):
    #             line_data.append(
    #
    #                     {
    #                         "product_id": line.product_id.id,
    #                         "name": line.name,
    #                         "account_id": line.account_id.id,
    #                         "split_method": line.split_method,
    #                         "price_unit": line.price_unit,
    #                         "partner_id":line.partner_id.id if line.partner_id else '',
    #                         "currency_id":line.currency_id.id if line.currency_id else line.company_id.currency_id.id,
    #
    #                     }
    #             )
    #             line.is_landed_cost_created = True
    #         for key, group in itertools.groupby(line_data, key=lambda x: (x['currency_id'])):
    #
    #             name = ''
    #             total = 0
    #             docs=[]
    #             for item in group:
    #
    #                 docs.append((0, 0, {
    #
    #                     "product_id": item["product_id"],
    #                     "name":  item["name"],
    #                     "account_id": item["account_id"],
    #                     "split_method":item["split_method"],
    #                     "price_unit":item["price_unit"],
    #                     "partner_id": item['partner_id'],
    #                     "currency_id":item["currency_id"],
    #                 }))
    #             landed_cost = self.env["stock.landed.cost"].create(
    #                 {
    #                     "date": datetime.now().date(),
    #                     "purchase_id": self.purchase_id.id,
    #                     "picking_ids": self.ids,
    #                     "cost_lines": docs,
    #                     "branch_id":self.purchase_id.branch_id.id if self.purchase_id.branch_id else ''
    #                 }
    #             )
    #             self.sudo().purchase_id.landed_costs_ids = [(4, landed_cost.id)]
    #             landed_cost.sudo().with_context({"is_purchase_auto_calculation": True}).button_validate()
    #     return res


class StockLandedCost(models.Model):
    _inherit = "stock.landed.cost"

    purchase_id = fields.Many2one("purchase.order")

    def compute_landed_cost(self):
        res = super(StockLandedCost, self).compute_landed_cost()
        if self.cost_lines and self.env.context.get("is_purchase_auto_calculation"):

            total_purchase_qty = 0
            total_product_weight = 0
            total_product_volume = 0

            for line in self.purchase_id.order_line:
                total_purchase_qty += line.product_qty
                total_product_weight += line.product_id.weight * line.product_qty
                total_product_volume += line.product_id.volume * line.product_qty

            purchase_order_line_ids = []
            prev_former_cost = 0
            for line in self.env["stock.valuation.adjustment.lines"].search(
                [("cost_line_id", "=", self.cost_lines[0].id)]
            ):
                purchase_line_id = self.env["purchase.order.line"].search(
                    [
                        ("product_id", "=", line.product_id.id),
                        ("order_id", "=", self.purchase_id.id),
                        ("id", "not in", purchase_order_line_ids),
                    ],
                    limit=1,
                    order="id asc",
                )
                purchase_order_line_ids.append(purchase_line_id.id)
                prev_former_cost += line.former_cost / line.quantity * purchase_line_id.product_qty

            purchase_order_line_ids = []
            cost_dict = {}
                    
            for line in self.valuation_adjustment_lines:
                purchase_line_id = self.env["purchase.order.line"].search(
                    [
                        ("product_id", "=", line.product_id.id),
                        ("order_id", "=", self.purchase_id.id),
                        ("id", "not in", purchase_order_line_ids),
                    ],
                    limit=1,
                    order="id asc",
                )
                purchase_order_line_ids.append(purchase_line_id.id)
                if (
                    line.cost_line_id.split_method == "equal"
                    and line.quantity != purchase_line_id.product_qty
                    and purchase_line_id.product_qty > 0
                ):
                    line.additional_landed_cost = (
                        line.quantity / purchase_line_id.product_qty * line.additional_landed_cost
                    )
                elif line.cost_line_id.split_method == "by_quantity":
                    line.additional_landed_cost = line.cost_line_id.price_unit / total_purchase_qty * line.quantity
                elif line.cost_line_id.split_method == "by_weight":
                    line.additional_landed_cost = (
                        line.cost_line_id.price_unit / total_product_weight * line.quantity * line.product_id.weight
                    )
                elif line.cost_line_id.split_method == "by_volume":
                    line.additional_landed_cost = (
                        line.cost_line_id.price_unit / total_product_volume * line.quantity * line.product_id.volume
                    )
                elif line.cost_line_id.split_method == "by_current_cost_price":
                    line.additional_landed_cost = line.cost_line_id.price_unit / prev_former_cost * line.former_cost
                if line.cost_line_id.id not in cost_dict:
                    cost_dict[line.cost_line_id.id] = line.additional_landed_cost
                else:
                    cost_dict[line.cost_line_id.id] += line.additional_landed_cost
            landed_cost_line_obj = self.env["stock.landed.cost.lines"]
            for key, value in cost_dict.items():
                landed_cost_line_obj.browse(key).write({"price_unit": value})
                
            net_cost_dict = {}
            for line in self.valuation_adjustment_lines:
                if line.product_id.id not in net_cost_dict:
                    net_cost_dict[line.product_id.id] = line.additional_landed_cost / line.quantity
                else:
                    net_cost_dict[line.product_id.id] += line.additional_landed_cost / line.quantity
                
            for key, value in net_cost_dict.items():
                purchaseline_id = self.env["purchase.order.line"].search(
                    [
                        ("product_id", "=", key),
                        ("order_id", "=", self.purchase_id.id),                    ],
                    limit=1,
                    order="id asc",
                )
                if purchaseline_id:
                    purchaseline_id.write({"line_product_landed_cost": value + purchaseline_id.price_unit})
                    
                    
        return res
