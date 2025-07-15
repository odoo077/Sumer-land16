from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    line_product_landed_cost = fields.Float("Cost", default=0.0)
    purchase_price = fields.Float()

    @api.depends('purchase_price', 'order_id.total_costs', 'order_id.total_qty')
    def get_price_unit(self):
        for rec in self:
            rec.price_unit = rec.purchase_price
            if rec.order_id:
                extra_price = 0
                if rec.order_id.total_qty:
                    # extra_price = rec.order_id.total_costs / rec.order_id.total_qty
                    rec.price_unit = rec.purchase_price + extra_price


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    landed_cost_lines = fields.One2many("purchase.landed.cost.line", "purchase_id", "Landed Costs")
    landed_costs_ids = fields.Many2many("stock.landed.cost", copy=False)

    total_costs = fields.Float("Total Cost", default=0.0, compute="compute_total_costs")
    total_with_costs = fields.Float("Total With Cost", default=0.0, compute="compute_total_costs")
    total_qty = fields.Float(compute="get_total_qty")

    @api.depends('order_line')
    def get_total_qty(self):
        for rec in self:
            rec.total_qty = 0
            total_qty = 0
            for line in rec.order_line:
                total_qty += line.product_qty
            rec.total_qty = total_qty

    def update_purchase_price(self):
        order_ids = self.env['purchase.order'].search([])

        for rec in order_ids.order_line:
            rec.price_unit = rec.purchase_price

    @api.depends('landed_cost_lines.price_unit', 'amount_total')
    def compute_total_costs(self):
        for rec in self:
            total_costs = 0.0
            if rec.landed_cost_lines:
                for line in rec.landed_cost_lines:
                    if line.price_unit > 0:
                        total_costs = total_costs + line.price_unit
            rec.total_costs = total_costs
            rec.total_with_costs = total_costs + rec.amount_total

    @api.onchange('landed_cost_lines', 'order_line')
    def on_change_compute_total_costs(self):
        for rec in self:
            total_costs = 0.0
            if rec.landed_cost_lines:
                for line in rec.landed_cost_lines:
                    if line.price_unit > 0:
                        total_costs = total_costs + line.price_unit
            rec.total_costs = total_costs
            rec.total_with_costs = total_costs + rec.amount_total

    def action_view_landed_costs(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock_landed_costs.action_stock_landed_cost")
        domain = [("id", "in", self.landed_costs_ids.ids)]
        context = dict(self.env.context, default_purchase_id=self.id)
        views = [
            (self.env.ref("ssq_purchase_auto_landed_cost_creation.view_stock_landed_cost_tree").id, "tree"),
            (False, "form"),
            (False, "kanban"),
        ]
        return dict(action, domain=domain, context=context, views=views)


class PurchaseLandedCost(models.Model):
    _name = "purchase.landed.cost.line"

    name = fields.Char("Description")
    product_id = fields.Many2one("product.product", "Product", domain=[("landed_cost_ok", "=", True)], required=True)

    split_method = fields.Selection(
        [
            ("equal", "Equal"),
            ("by_quantity", "By Quantity"),
            ("by_current_cost_price", "By Current Cost"),
            ("by_weight", "By Weight"),
            ("by_volume", "By Volume"),
        ],
        "Split Method",
        default="equal",
        required=True,
    )
    currency_id = fields.Many2one('res.currency', string="Currency")
    amount = fields.Float("Amount")
    rate = fields.Float("Rate" )
    price_unit = fields.Float("Cost")
    payment_value = fields.Float("Payment Amount")
    purchase_id = fields.Many2one("purchase.order")
    state = fields.Selection(related="purchase_id.state")
    branch_id = fields.Many2one(related="purchase_id.company_id")
    is_landed_cost_created = fields.Boolean(default=False)
    partner_id = fields.Many2one("res.partner", string="الوكيل")
    account_id = fields.Many2one("account.account", "Account", domain="[('company_id','=',branch_id)]")
    payment_state = fields.Boolean()
    @api.onchange("account_id", "partner_id")
    def _onchnage_account_id(self):
        if self.partner_id:
            if self.account_id and self.account_id.internal_type != 'payable':
                self.account_id = ''
            domain = {'account_id': [('internal_type', '=', 'payable')]}
            return {'domain': domain}

    @api.onchange('currency_id', 'amount', 'rate')
    def cal_cost_in_other_currency(self):
        for rec in self:
            if rec.currency_id.rate > 0:
                rec.price_unit = rec.amount / rec.currency_id.rate
                rec.rate=rec.currency_id.rate

    def unlink(self):
        for record in self:
            if record.is_landed_cost_created:
                raise UserError(_("You cannot delete a posted landed cost entry !!!"))
        return super(PurchaseLandedCost, self).unlink()

    @api.onchange("product_id")
    def onchange_product_id(self):
        self.name = self.product_id.name
        self.account_id = (
                self.product_id.property_account_expense_id.id
                or self.product_id.categ_id.property_account_expense_categ_id.id
        )

    def create_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.payment',
            'context': {'default_cost_id': self.id, 'default_amount': self.amount, 'default_payment_type': 'outbound',
                        'default_partner_type': 'supplier', 'search_default_outbound_filter': 1,'default_destination_account_id':self.account_id.id,
                        'default_move_journal_types': ('bank', 'cash'), 'default_partner_id':self.partner_id.id,'default_currency_id':self.currency_id.id},

            'target': 'new',
        }
