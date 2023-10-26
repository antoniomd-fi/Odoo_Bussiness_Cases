from odoo import fields, models


class ProjectCollaborator(models.Model):
    _inherit = 'project.collaborator'
    _description = 'Collaborators in site shared'

    project_id = fields.Many2one('project.project', 'Site Shared', domain=[('privacy_visibility', '=', 'portal')], required=True, readonly=True)
