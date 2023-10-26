from odoo import fields, models


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'
    _description = 'Milestone Stage'

    project_ids = fields.Many2many('project.project', 'project_task_type_rel', 'type_id', 'project_id', string='Sites',
        default=lambda self: self._get_default_project_ids(),
        help="Sites in which this stage is present. If you follow a similar workflow in several sites,"
            " you can share this stage among them and get consolidated information this way.")
    mail_template_id = fields.Many2one(
        'mail.template',
        string='Email Template',
        domain=[('model', '=', 'project.task')],
        help="If set, an email will be automatically sent to the customer when the milestone reaches this stage.")
    fold = fields.Boolean(string='Folded in Kanban',
        help='If enabled, this stage will be displayed as folded in the Kanban view of your milestone. Milestones in a folded stage are considered as closed (not applicable to personal stages).')
    rating_template_id = fields.Many2one(
        'mail.template',
        string='Rating Email Template',
        domain=[('model', '=', 'project.task')],
        help="If set, a rating request will automatically be sent by email to the customer when the milestone reaches this stage. \n"
             "Alternatively, it will be sent at a regular interval as long as the milestone remains in this stage, depending on the configuration of your site. \n"
             "To use this feature make sure that the 'Customer Ratings' option is enabled on your site.")

class Project(models.Model):
    _inherit = "project.project"
    _description = "Site"

    name = fields.Char("Name", index='trigram', required=True, tracking=True, translate=True, default_export_compatible=True,
        help="Name of your site. It can be anything you want e.g. the name of a customer or a service.")
    description = fields.Html(help="Description to provide more information and context about this site")
    active = fields.Boolean(default=True,
        help="If the active field is set to False, it will allow you to hide the site without removing it.")
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account", copy=False, ondelete='set null',
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", check_company=True,
        help="Analytic account to which this site, its milestones and its timesheets are linked. \n"
            "Track the costs and revenues of your site by setting this analytic account on your related documents (e.g. sales orders, invoices, purchase orders, vendor bills, expenses etc.).\n"
            "This analytic account can be changed on each milestone individually if necessary.\n"
            "An analytic account is required in order to use timesheets.")

    is_favorite = fields.Boolean(compute='_compute_is_favorite', inverse='_inverse_is_favorite', compute_sudo=True,
        string='Show Site on Dashboard')
    label_tasks = fields.Char(string='Use Milestone as', default='Milestone', translate=True,
        help="Name used to refer to the milestones of your site e.g. tasks, tickets, sprints, etc...")
    tasks = fields.One2many('project.task', 'project_id', string="Milestones Activities")
    type_ids = fields.Many2many('project.task.type', 'project_task_type_rel', 'project_id', 'type_id', string='Milestones Stages')
    task_count = fields.Integer(compute='_compute_task_count', string="Milestones Count")
    task_ids = fields.One2many('project.task', 'project_id', string='Milestone',
                               domain=[('is_closed', '=', False)])
    user_id = fields.Many2one('res.users', string='Site Manager', default=lambda self: self.env.user, tracking=True)
    alias_id = fields.Many2one('mail.alias', string='Alias', ondelete="restrict", required=True,
        help="Internal email associated with this site. Incoming emails are automatically synchronized "
             "with Milestones (or optionally Issues if the Issue Tracker module is installed).")

    privacy_visibility = fields.Selection([
            ('followers', 'Invited internal users'),
            ('employees', 'All internal users'),
            ('portal', 'Invited portal users and all internal users'),
        ],
        string='Visibility', required=True,
        default='portal',
        help="People to whom this project and its milestones will be visible.\n\n"
            "- Invited internal users: when following a project, internal users will get access to all of its milestones without distinction. "
            "Otherwise, they will only get access to the specific milestones they are following.\n "
            "A user with the project > administrator access right level can still access this project and its milestones, even if they are not explicitly part of the followers.\n\n"
            "- All internal users: all internal users can access the project and all of its milestones without distinction.\n\n"
            "- Invited portal users and all internal users: all internal users can access the project and all of its milestones without distinction.\n"
            "When following a project, portal users will get access to all of its milestones without distinction. Otherwise, they will only get access to the specific milestones they are following.\n\n"
            "When a project is shared in read-only, the portal user is redirected to their portal. They can view the milestones, but not edit them.\n"
            "When a project is shared in edit, the portal user is redirected to the kanban and list views of the milestones. They can modify a selected number of fields on the milestones.\n\n"
            "In any case, an internal user with no project access rights can still access a task, "
            "provided that they are given the corresponding URL (and that they are part of the followers if the project is private).")

    date = fields.Date(string='Expiration Date', index=True, tracking=True,
        help="Date on which this project ends. The timeframe defined on the site is taken into account when viewing its planning.")
    allow_subtasks = fields.Boolean('Sub-milestones', default=lambda self: self.env.user.has_group('project.group_subtask_project'))
    allow_recurring_tasks = fields.Boolean('Recurring Milestones', default=lambda self: self.env.user.has_group('project.group_project_recurring_tasks'))
    allow_task_dependencies = fields.Boolean('Milestones Dependencies', default=lambda self: self.env.user.has_group('project.group_project_task_dependencies'))
    allow_milestones = fields.Boolean('Milestones', default=lambda self: self.env.user.has_group('project.group_project_milestone'))
    task_properties_definition = fields.PropertiesDefinition('Milestones Properties')

    #NEW FIELDS
    deadline_date = fields.Datetime(string="Deadline Date")
    budget = fields.Float(default=0.0)
    project_size = fields.Selection(
         [('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')],
        string='Project Size',
        required=True,
        default='small'
    )
    #stage_id already exist
    stage= fields.Many2one('project.project.stage', default=1)



class Task(models.Model):
    _inherit = "project.task"
    _description = "Milestone"

    tag_ids = fields.Many2many('project.tags', string='Tags',
        help="You can only see tags that are already present in your site. If you try creating a tag that is already existing in other sites, it won't generate any duplicates.")
    date_assign = fields.Datetime(string='Assigning Date', copy=False, readonly=True,
        help="Date on which this milestone was last assigned (or unassigned). Based on this, you can get statistics on the time it usually takes to assign milestones.")
  
    date_last_stage_update = fields.Datetime(string='Last Stage Update',
        index=True,
        copy=False,
        readonly=True,
        help="Date on which the stage of your milestone has last been modified.\n"
            "Based on this information you can identify milestones that are stalling and get statistics on the time it usually takes to move milestone from one stage to another.")
    project_id = fields.Many2one('project.project', string='Site', recursive=True,
        compute='_compute_project_id', store=True, readonly=False, precompute=True,
        index=True, tracking=True, check_company=True, change_default=True)
    subtask_planned_hours = fields.Float("Sub-milestone Planned Hours", compute='_compute_subtask_planned_hours',
        help="Sum of the hours allocated for all the sub-milestone (and their own sub-milestone) linked to this milestone. Usually less than or equal to the allocated hours of this milestone.")
    

    email_cc = fields.Char(help='Email addresses that were in the CC of the incoming emails from this milestone and that are not currently linked to an existing customer.')
    manager_id = fields.Many2one('res.users', string='Site Manager', related='project_id.user_id', readonly=True)
    rating_active = fields.Boolean(string='Site Rating Status', related="project_id.rating_active")

    parent_id = fields.Many2one('project.task', string='Parent Milestone', index=True)
    ancestor_id = fields.Many2one('project.task', string='Ancestor Milestone', compute='_compute_ancestor_id', index='btree_not_null', recursive=True, store=True)
    child_ids = fields.One2many('project.task', 'parent_id', string="Sub-milestones")
    allow_subtasks = fields.Boolean(string="Allow Sub-milestones", related="project_id.allow_subtasks", readonly=True)
    subtask_count = fields.Integer("Sub-milestones Count", compute='_compute_subtask_count')

    project_privacy_visibility = fields.Selection(related='project_id.privacy_visibility', string="Site Visibility")
    dependent_tasks_count = fields.Integer(string="Dependent Milestones", compute='_compute_dependent_tasks_count')
    recurring_count = fields.Integer(string="Milestone in Recurrence", compute='_compute_recurring_count')

    # Account analytic
    analytic_account_id = fields.Many2one('account.analytic.account', ondelete='set null', compute='_compute_analytic_account_id', store=True, readonly=False,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", check_company=True,
        help="Analytic account to which this milestone and its timesheets are linked.\n"
            "Track the costs and revenues of your milestone by setting its analytic account on your related documents (e.g. sales orders, invoices, purchase orders, vendor bills, expenses etc.).\n"
            "By default, the analytic account of the project is set. However, it can be changed on each milestone individually if necessary.")
    project_analytic_account_id = fields.Many2one('account.analytic.account', string='Site Analytic Account', related='project_id.analytic_account_id')
