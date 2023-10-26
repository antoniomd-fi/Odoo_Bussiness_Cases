from odoo import api, fields, models, _

class DynamicRequirementFieldLine(models.Model):
    _name = 'dynamic.requirement.field.line'

    sequence = fields.Integer(default=10)
    requirement_mandatory_project = fields.Many2one("dynamic.requirement.field")
    stage = fields.Many2one("project.project.stage")
    mandatory_fields = fields.Many2many("ir.model.fields")
    custom_warning_message = fields.Char(String="Custom Warning Message", required=True)
    company = fields.Many2one("res.company", default=lambda self: self.env.user.company_id)