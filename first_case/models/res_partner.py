from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    task_ids = fields.One2many('project.task', 'partner_id', string='Milestones')
    task_count = fields.Integer(compute='_compute_task_count', string='# Milestones')
