from odoo import fields, models


class ResCompany(models.Model):
    _name = "res.company"
    _inherit = "res.company"

    analytic_plan_id = fields.Many2one(
        'account.analytic.plan',
        string="Default Plan",
        check_company=True,
        readonly=False,
        compute="_compute_analytic_plan_id",
        help="Default Plan for a new analytic account for Sites")
