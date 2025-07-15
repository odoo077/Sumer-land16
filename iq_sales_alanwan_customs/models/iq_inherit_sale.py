# -*- coding: utf-8 -*-

from odoo import models, fields, api,SUPERUSER_ID,_,exceptions


class iq_inherit_saleorder(models.Model):
    _inherit = 'sale.order'
    
    
    iq_address = fields.Char(related='partner_id.street',string='Address')
    iq_phone = fields.Char(related='partner_id.phone',string='Phone')

    iq_discount_type = fields.Selection([('percent','Percentage'),('amount','Amount')],
                                        string='Discount Type',readonly=True,
                                        states={'draft': [('readonly',False)],'sent': [('readonly',False)]},
                                        default='percent')
    iq_discount_amount = fields.Float('Discount Amount',readonly=True,
                                      states={'draft': [('readonly',False)],'sent': [('readonly',False)]})


    @api.onchange('iq_discount_amount','iq_discount_type')
    def iq_get_discount(self):
        if self.iq_discount_amount != 0:
            iq_count = 0
            line_disc = 0
            disc = 0
            for x in self.order_line:
                iq_count = iq_count + 1
            if self.iq_discount_type == 'percent':
                line_disc = self.iq_discount_amount
            else:
                line_disc = self.iq_discount_amount / iq_count

            if line_disc > 0:
                for x in self.order_line:
                    if self.iq_discount_type == 'percent':
                        x.write({
                            'iq_disc': line_disc,
                            'iq_discount_type': self.iq_discount_type,
                            'discount': line_disc,
                        })
                    if self.iq_discount_type == 'amount':
                        if x.price_unit != 0:

                            # line_per = float_round(((line_disc / x.price_unit) * 100),precision_digits=20)
                            x.write({
                                'iq_disc': line_disc,
                                'iq_discount_type': self.iq_discount_type,
                            })


