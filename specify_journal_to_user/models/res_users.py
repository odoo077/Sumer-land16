from odoo import api, fields, models


class Users(models.Model):
    _inherit = "res.users"

    def _get_default_journal_id(self):
        if self.env.user.assigned_journal_id:
            return self.env.user.assigned_journal_id
        else:
            domain = [('company_id', '=', self.env.user.company_id.id),('type', 'in', ('cash','bank'))]
            journal = self.env['account.journal'].search(domain, limit=1,order='id desc')
            if journal:
                return journal.id
            else:
                return False;

    assigned_journal_id = fields.Many2one(
        "account.journal",
        string="Sales Journal",
        default=_get_default_journal_id,
        domain="[('company_id', '=', company_id),('type', 'in', ('cash','bank'))]",
        help="Specifying Sales Journal to User.",
    )

    assigned_journal_ids = fields.One2many('res.users.journals', 'user_id', string='Journal Ids')


class UserMultiJournals(models.Model):
    _name = 'res.users.journals'
    _description = 'Multi User Journals'

    user_id = fields.Many2one('res.users', string="User",ondelete="cascade",readonly=True )
    journal_id = fields.Many2one('account.journal',domain="[('type', 'in', ('cash','bank'))]", string="Journal")
    currency_id = fields.Many2one('res.currency',related="journal_id.currency_id", string="Currency")
