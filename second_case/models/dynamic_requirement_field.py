from odoo import api, fields, models, _

class DynamicRequirementField(models.Model):
    _name = 'dynamic.requirement.field'

    sequence = fields.Integer(default=10)
    type = fields.Selection(
        [('site', 'Site'), ('milestone', 'Milestone')],
        required=True,
    )
    name = fields.Char(default="New", copy=False, required=True)
    active = fields.Boolean(default=True)
    mandatory_project_line = fields.One2many("dynamic.requirement.field.line", "requirement_mandatory_project")
    company = fields.Many2one("res.company", default=lambda self: self.env.user.company_id)
    project_ids = fields.One2many("project.project", "requirement")