from odoo import models, fields, api, exceptions, _
# from odoo.exceptions import ValidationError

class ProductSumerTemplateaMiles(models.Model):
    _inherit = 'product.template'

    key_no = fields.Char(string=' رقم المفتاح')
    currency_device_no = fields.Char(string='رقم جهاز العملة')
    location = fields.Char(string='الموقع')


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    key_no = fields.Char(string=' رقم المفتاح')
    currency_device_no = fields.Char(string='رقم جهاز العملة')
    location = fields.Char(string='الموقع')

class AccountMoveIInherit(models.Model):
    _inherit = 'account.move'

    driver_name = fields.Char(string='اسم السائق')

class SaleOrderInherit1(models.Model):
    _inherit = 'sale.order'

    def _create_invoices(self, grouped=False, final=False, date=None):
        res=super(SaleOrderInherit1, self)._create_invoices(grouped=False, final=False, date=None)
        for rec in res:
            rec.wrranty_date_start=self.wrranty_date_start
            rec.wrranty_date_end=self.wrranty_date_end

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    lot_serial = fields.Many2one('stock.production.lot',string='Lot/Serial',domain="[('product_id','=',product_id)]")
    key_no = fields.Char(string=' رقم المفتاح',related='lot_serial.key_no')
    currency_device_no = fields.Char(string='رقم جهاز العملة',related='lot_serial.currency_device_no')
    location = fields.Char(string='الموقع',related='lot_serial.location')

    def _prepare_invoice_line(self, **optional_values):
        res=super(SaleOrderLineInherit, self)._prepare_invoice_line(**optional_values)
        if self.lot_serial:
            res['lot_serial']=self.lot_serial.id
        return res

class InvoiceUpdate(models.Model):
    _inherit = 'account.move'

    wrranty_date_start = fields.Date(string='بداية تاريخ الضمان')
    wrranty_date_end = fields.Date(string='انتهاء تاريخ الضمان')


class InvoiceMoveLinesUpdate(models.Model):
    _inherit = 'account.move.line'

    lot_serial = fields.Many2one('stock.production.lot',string='Lot/Serial')
    key_no = fields.Char(string=' رقم المفتاح', related='lot_serial.key_no')
    currency_device_no = fields.Char(string='رقم جهاز العملة', related='lot_serial.currency_device_no')
    location = fields.Char(string='الموقع', related='lot_serial.location')

