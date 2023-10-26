from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_hr_timesheet = fields.Boolean(string="Milestones Logs")
    group_subtask_project = fields.Boolean("Sub-milestones", implied_group="project.group_subtask_project")
    group_project_stages = fields.Boolean("Site Stages", implied_group="project.group_project_stages")
    group_project_recurring_tasks = fields.Boolean("Recurring Milestones", implied_group="project.group_project_recurring_tasks")
    group_project_task_dependencies = fields.Boolean("Milestones Dependencies", implied_group="project.group_project_task_dependencies")
    group_project_milestone = fields.Boolean('Milestones', implied_group='project.group_project_milestone', group='base.group_portal,base.group_user')
