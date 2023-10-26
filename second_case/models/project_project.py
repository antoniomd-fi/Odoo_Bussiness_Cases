from odoo import fields, models, api, _

class Project(models.Model):
    _inherit = "project.project"
    _description = "Site"

    requirement = fields.Many2one("dynamic.requirement.field")

    @api.onchange('stage')
    def _onchange_stage_id(self):
        for project in self:
            if project.requirement:
                requirement_stage = project.requirement.mandatory_project_line.stage
                mandatory_fields = project.requirement.mandatory_project_line.mandatory_fields

                if (project.stage == requirement_stage):
                    missing_fields = mandatory_fields.filtered(lambda field: not project[field.name])

                    if missing_fields:
                        warning_message = _(project.requirement.mandatory_project_line.custom_warning_message)
                        return {
                            'warning': {
                            'title': _('Warning'),
                            'message': warning_message,
                            }
                    }

            
