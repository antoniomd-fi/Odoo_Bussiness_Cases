from odoo import fields, models

class ProjectTaskRecurrence(models.Model):
    _inherit = 'project.task.recurrence'
    _description = 'Milestone Recurrence'

    recurrence_left = fields.Integer(string="Number of Milestones Left to Create", copy=False)
