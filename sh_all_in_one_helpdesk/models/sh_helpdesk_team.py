# -*- coding: utf-8 -*-
from odoo import models, fields, api, api

class HelpdeskTeam(models.Model):
    _name = 'sh.helpdesk.team'
    _description = 'Helpdesk Team'
    _inherit = ['mail.thread', 'mail.alias.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    team_head = fields.Many2one('res.users', string='Team Leader', tracking=True)
    sh_resource_calendar_id = fields.Many2one('resource.calendar', string='Working Hours')
    member_ids = fields.Many2many('res.users', string='Team Members')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    sla_count = fields.Integer(string='SLA Count', compute='_compute_sla_count')
    active = fields.Boolean(default=True)
    alias_id = fields.Many2one('mail.alias', string='Alias', ondelete='restrict')
    alias_domain = fields.Char(compute='_compute_alias_domain')
    
    @api.depends()
    def _compute_alias_domain(self):
        for record in self:
            record.alias_domain = self.env["ir.config_parameter"].sudo().get_param("mail.catchall.domain")
    
    @api.depends('name')
    def _compute_sla_count(self):
        for team in self:
            team.sla_count = self.env['sh.helpdesk.sla'].search_count([('team_id', '=', team.id)])
            
    def action_view_sla(self):
        self.ensure_one()
        return {
            'name': 'SLA Policies',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sh.helpdesk.sla',
            'domain': [('team_id', '=', self.id)],
            'context': {'default_team_id': self.id},
        }
        
    def action_edit_alias(self):
        self.ensure_one()
        if not self.alias_id:
            self.alias_id = self.env['mail.alias'].create({
                'alias_name': False,
                'alias_model_id': self.env['ir.model']._get('sh.helpdesk.ticket').id,
                'alias_parent_model_id': self.env['ir.model']._get('sh.helpdesk.team').id,
                'alias_parent_thread_id': self.id,
                'alias_defaults': {'team_id': self.id},
            })
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.alias',
            'target': 'new',
            'res_id': self.alias_id.id,
        }
