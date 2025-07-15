# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from datetime import datetime


class PaymentReceipt(models.Model):

    _inherit = 'account.payment'

    def _compute_amount_in_word(self):
        for rec in self:
            rec.num_word = str(rec.currency_id.with_context(lang='ar_001').amount_to_text(rec.amount))

    def _compute_seq_last_number(self):
        for rec in self:
            if rec.name and rec.state == 'posted':
                new_seq = rec.name.split('/')[3]
                print(new_seq)
                rec.seq_last_number = new_seq
            else:
                rec.seq_last_number = '/'

    num_word = fields.Char(string=_("Amount In Words:"), compute='_compute_amount_in_word')
    seq_last_number = fields.Char(string="New Sequence", compute='_compute_seq_last_number')

