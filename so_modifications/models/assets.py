from datetime import datetime
from odoo import models, fields, api, tools, exceptions, _
from odoo.exceptions import ValidationError

class AccountAssetsInheritUpdate(models.Model):
    _inherit = "account.asset"

    machine_sn = fields.Char(string='Machine SN.',track_visibility='onchange')
    kelon_number = fields.Char(string='Kelon number',track_visibility='onchange')
    bt11_sn = fields.Char(string='BT11 SN.',track_visibility='onchange')
    location_name = fields.Char(string='Name of location',track_visibility='onchange')
    wrranty_date_start = fields.Date(string='Start Data',track_visibility='onchange')
    wrranty_date_end = fields.Date(string='End Date',track_visibility='onchange')
    remain_days = fields.Char(string='Days Remaining', compute='calculate_date_in_days',track_visibility='onchange')
    warranty = fields.Selection([
        ('under', 'Under warranty'),
        ('out', 'Out of warranty'),
    ],string='Warranty',compute='calculate_date_in_days',track_visibility='onchange')
    address = fields.Text(string='Address',track_visibility='onchange')
    owner = fields.Many2one('owner.name',string='Owner name',track_visibility='onchange')

    service_dukan = fields.Selection([
        ('yes', 'True'),
        ('no', 'False'),
    ], string='Under Dukani Service',track_visibility='onchange')
    model = fields.Char(string='Machine Model',track_visibility='onchange')
    governorate = fields.Many2one('res.country.state',string='Governorate',track_visibility='onchange')
    machine_kind = fields.Many2one('machine.kind',string='Kind of machine',track_visibility='onchange')
    counter = fields.Char(string='Counter',track_visibility='onchange')



    @api.depends('wrranty_date_end','remain_days')
    def calculate_date_in_days(self):
        for rec in self:
            rec.remain_days=False
            rec.warranty = 'under'
            today = fields.Date.today()
            if rec.wrranty_date_end :
                d1 = datetime.strptime(str(today), '%Y-%m-%d')
                d2 = datetime.strptime(str(rec.wrranty_date_end), '%Y-%m-%d')
                d3 = d2 - d1
                rec.remain_days = str(d3.days)
                if int(rec.remain_days) >0:
                    rec.warranty='under'
                else:
                    rec.warranty = 'out'



class OwnerUpdate(models.Model):
    _name = "owner.name"

    name = fields.Char('Name')



class MachineKindUpdate(models.Model):
    _name = "machine.kind"

    name = fields.Char('Name')