from datetime import datetime

from odoo import models, fields, api, tools, exceptions, _
from odoo.exceptions import ValidationError

class WrrantyTypeUpdate(models.Model):
    _name = "wrranty.type"

    name = fields.Char('Name')

class SOInheritUpdate(models.Model):
    _inherit = "sale.order"

    wrranty_date_start = fields.Date(string='بداية تاريخ الضمان')
    wrranty_date_end = fields.Date(string='انتهاء تاريخ الضمان')
    remain_days = fields.Char(string='عدد الايام المتبقية',compute='calculate_date_in_days')
    wrranty_type = fields.Many2one('wrranty.type',string='نوع الضمان')

    @api.depends('wrranty_date_end')
    def calculate_date_in_days(self):
        for rec in self:
            rec.remain_days=False
            today = fields.Date.today()
            if rec.wrranty_date_end :
                d1 = datetime.strptime(str(today), '%Y-%m-%d')
                d2 = datetime.strptime(str(rec.wrranty_date_end), '%Y-%m-%d')
                d3 = d2 - d1
                rec.remain_days = str(d3.days)

    # @api.depends('state')
    # def cal_seq_for_treasury(self):
    #     list = []
    #     for line in self:
    #         if line.state == 'journal':
    #             max_seq = self.env['paym.account'].search(
    #                 [('short_code', '=', line.short_code), ('safe_seq', '!=', '')])
    #             if max_seq:
    #                 for rec in max_seq:
    #                     mm = rec.safe_seq.split('/')
    #                     second = int(mm[1])
    #                     list.append(second)
    #                 counter = (max(list))
    #                 new = counter + 1
    #                 line.safe_seq = str(line.journal.code) + '/' + str(new)
    #
    #             else:
    #                 line.safe_seq = str(line.journal.code) + '/' + str(1)
