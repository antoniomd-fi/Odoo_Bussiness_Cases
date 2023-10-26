from odoo import fields, models

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    _description = 'Analytic Account'

    project_ids = fields.One2many('project.project', 'analytic_account_id', string='Sites')
    project_count = fields.Integer("Site Count", compute='_compute_project_count')
