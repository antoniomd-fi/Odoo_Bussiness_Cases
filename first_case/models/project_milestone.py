from odoo import fields, models

class ProjectMilestone(models.Model):
    _inherit = 'project.milestone'
    _description = "Site Milestone"

    task_ids = fields.One2many('project.task', 'milestone_id', 'Milestones')

    task_count = fields.Integer('# of Milestones', compute='_compute_task_count', groups='project.group_project_milestone')
