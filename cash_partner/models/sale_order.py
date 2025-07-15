from odoo import fields, models, api

import datetime
class Sale(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(Sale,self).action_confirm()
        if self.partner_id.is_cash:
            state_pick=''
            for rec in self.picking_ids:
                if rec.location_dest_id.usage=='customer':
                    rec.action_confirm()
                    if rec.state=='assigned':
                        print('yees')
                        immediate_transfer = self.env['stock.immediate.transfer'].sudo().create({

                        })
                        self.env['stock.immediate.transfer.line'].sudo().create({
                            'immediate_transfer_id': immediate_transfer.id,
                            'picking_id': rec.id,
                            'to_immediate': True
                        })
                        immediate_transfer.sudo().process()
                        rec.button_validate()
                        state_pick = 'done'
            if state_pick=='done':
                move_id = self._create_invoices()
                for inv in self.invoice_ids:
                    inv.sudo().action_post()
                    # if self.pricelist_id.journal_id:
                    #     pmt_wizard = self.env['account.payment.register'].with_context(active_model='account.move',
                    #                                                                    active_ids=inv.id).create({
                    #         # 'payment_date': datetime.datetime.date(),
                    #         'journal_id': self.pricelist_id.journal_id.id
                    #     })
                    #     pmt_wizard._create_payments()
        return res

