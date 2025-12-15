from odoo import api, models, fields
from odoo.exceptions import ValidationError

class Course(models.Model):
    _name = "academy.course"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, tracking=True)
    code = fields.Char(required=1, index=True) #uppercase conts
    description = fields.Text()
    instructor_id = fields.Many2one(
        'res.partner', string="Instructor"
    )
    category_id = fields.Many2one('academy.course.category')
    duration_hours = fields.Float()
    max_students = fields.Integer(default=20)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        tracking=True,
    )
    start_date = fields.Date(tracking=True)
    end_date = fields.Date(tracking=True)
    enrollment_ids = fields.One2many('academy.enrollment', 'course_id', string='Enrollments')

    #computed fields
    enrolled_count = fields.Integer(compute='_compute_enrolled_count', store=True)
    available_seats = fields.Integer(compute='_compute_available_seats', store=True)
    is_full = fields.Boolean(compute='_compute_is_full', store=True)
    
    #related fields
    instructor_name = fields.Char(related='instructor_id.name',string="Instructor name", store=True)


    #sql constraints
    _sql_constraints = [
        ("unique_code", "unique(code)", "Code must be unique!"),
    ]

    @api.depends('enrollment_ids')
    def _compute_enrolled_count(self):
        for rec in self:
            #count only when state is confirmed
            rec.enrolled_count = len(rec.enrollment_ids.filtered(lambda e: e.state == 'confirmed'))

    @api.depends('max_students', 'enrolled_count')
    def _compute_available_seats(self):
        for rec in self:
            rec.available_seats = rec.max_students - rec.enrolled_count

    @api.depends('available_seats')
    def _compute_is_full(self):
        for rec in self:
            rec.is_full = (rec.available_seats <= 0)        

    @api.constrains('code')
    def _check_uppercase(self):
        for rec in self:
            if rec.code and not rec.code.isupper():
                raise ValidationError("Code must be uppercase")


    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_data and rer.start_date > rec.end_date:
                raise ValidationError("Start date must be before end date")

    @api.constrains('max_students')
    def _check_max_students(self):
        for rec in self:
            if rec.max_students <= 0 :
                raise ValidationError("Max Students must be greater than 0")


    def action_publish(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'published'
            else:
                raise ValidationError("Only draft courses can be published.")

    def action_start(self):
        for rec in self:
            if rec.state == 'published':
                rec.state = 'in_progress'
            else:
                raise ValidationError("Only published courses can be started.")

    def action_complete(self):
        for rec in self:
            if rec.state == 'in_progress':
                rec.state = 'done'
            else:
                raise ValidationError("Only in-progress courses can be completed.")                

    #it should depends on the logic if all states could be cancelled or not
    def action_cancel(self):
        for rec in self:
            if rec.state in ['in_progress','done']:
                raise ValidationError("In-progress courses cannot be cancelled.")
            rec.state = 'cancelled'
            #reset available seats when cancelled
            rec.available_seats = rec.max_students


    def action_show_enrollments(self):
    # return an action or wizard
        return {
            'name': 'Enrollments',
            'type': 'ir.actions.act_window',
            'res_model': 'academy.enrollment',
            'view_mode': 'tree,form',
            'domain': [('course_id','=', self.id)],
        }
