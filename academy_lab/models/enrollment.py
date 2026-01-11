from odoo import api , models, fields
from odoo.exceptions import ValidationError

class Enrollment(models.Model):
    _name = 'academy.enrollment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Many2one('res.partner', required= True)
    course_id = fields.Many2one('academy.course', required=True)
    enrollment_date = fields.Date(default=fields.Date.context_today)
    state = fields.Selection(
        [('draft','Draft' ),
        ('confirmed', 'Confirmed'), 
        ('cancelled','Cancelled'),
        ('completed', 'Completed')
        ],
        string='Status',
        default='draft',
        tracking=True
    )
    grade = fields.Float(string='Grade')
    attendance_percentage = fields.Float(string="Attendance (%)")  # value 0-100
    notes = fields.Text()
    
    #related fields
    student_name = fields.Char(related='student_id.name', store=True)
    course_name = fields.Char(related='course_id.name', store=True)
    course_code = fields.Char(related='course_id.code', store=True)

    #wizard_fields
    invoice_id = fields.Many2one('account.move', readonly=True)

    #computed fields
    passed = fields.Boolean(
        string='Passed',
        compute='_compute_passed',
        store=True
    )

    _sql_constraints = [
        ('unique_enrollment', 'unique(student_id, course_id)', 'A student can only enroll in a course once.')
    ]

    @api.constrains('attendance_percentage','grade')
    def _check_values(self):
        for rec in self:
            if rec.attendance_percentage < 0 or rec.attendance_percentage > 100:
                raise ValueError("Attendance percentage must be between 0 and 100")
            if rec.grade < 0 or rec.grade > 100:
                raise ValueError("Grade must be between 0 and 100")

    # @api.constrains('course_id','state')
    # def _check_course_seates_availability(self):
    #     for rec in self:
    #         if rec.course_id.available_seats == 0 :
    #             raise ValidationError(
    #                 f"No available seats in course '{rec.course_id.code}'!"
    #             )


    @api.depends('grade', 'attendance_percentage')
    def _compute_passed(self):
        for rec in self:
            if rec.grade >= 60 and rec.attendance_percentage >= 75:
                rec.passed = True
            else:
                rec.passed = False            



    def action_confirm(self):
        for enrollmnt in self:
            if enrollmnt.state != 'draft': 
                raise ValidationError("Cannot confirm the enrollment !")
            
            confirmed_enrolls = len(enrollmnt.course_id.enrollment_ids.filtered(lambda e:e.state == 'confirmed'))

            if confirmed_enrolls >= enrollmnt.course_id.max_students:
                raise ValidationError("Cannot confirm enrollment. No available seats in the course.")
            enrollmnt.state = 'confirmed'


    def action_cancel(self):
        for enrollmnt in self:
            if enrollmnt.state not in  ['confirmed','draft']:
                raise ValidationError("Only confirmed enrollments can be cancelled.")
            enrollmnt.state = 'cancelled'


    def action_complete(self):
        for enrollmnt in self:
            if enrollmnt.state != 'confirmed':
                raise ValidationError("Only confirmed enrollments can be completed.")
            enrollmnt.state = 'completed'      


    def action_view_invoices(self):
        self.ensure_one()
        if not self.invoice_id.id:
            raise ValidationError("No invoices there")
        return {
            "type" : 'ir.actions.act_window',
            "name": "Invoices",
            "res_model" : "account.move",
            "view_mode" : "list,form",
            "domain" : [
                ("id" , '=' ,self.invoice_id.id)
            ]
        }        
    
    def action_open_filter_print_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('academy_lab.print_filltered_enrollment_action')
        action['context'] = { 'active_id': self.ids,
                              'active_model': self._name,
                              'filter_by': 'enrollment'} #pass the current course name 
        
        return action 