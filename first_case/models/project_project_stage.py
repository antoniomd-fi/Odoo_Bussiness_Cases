from odoo import fields, models

class ProjectProjectStage(models.Model):
    _inherit = 'project.project.stage'
    _description = 'Site Stage'

    mail_template_id = fields.Many2one('mail.template', string='Email Template', domain=[('model', '=', 'project.project')],
        help="If set, an email will be automatically sent to the customer when the site reaches this stage.")
    fold = fields.Boolean('Folded in Kanban',
        help="If enabled, this stage will be displayed as folded in the Kanban view of your sites. Sites in a folded stage are considered as closed.")
    project_ids = fields.One2many("project.project", "stage")
    project_ids = fields.One2many("dynamic.requirement.field.line", "stage")