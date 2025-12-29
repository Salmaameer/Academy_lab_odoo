from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    is_student  = fields.Boolean()
    is_instructor = fields.Boolean()

    instructor_course_ids = fields.One2many(
        'academy.course',
        'instructor_id',
        string='Courses'
    )

    student_enrollment_ids = fields.One2many(
        'academy.enrollment',
        'student_id',
        string='Enrollments'
    )

    total_courses_enrolled = fields.Integer(
        compute='_compute_courses_enrolled',
        string='Number of Courses',
        store=True
    )

    total_courses_teaching = fields.Integer(
        compute='_compute_courses_teaching',
        string='Number of Courses Teaching',
        store=True )

    @api.depends('student_enrollment_ids')
    def _compute_courses_enrolled(self):
        for partner in self:
            partner.total_courses_enrolled = len(partner.student_enrollment_ids.filtered(lambda e:e.state == 'confirmed'))


    @api.depends('instructor_course_ids')
    def _compute_courses_teaching(self):
        for partner in self:
            partner.total_courses_teaching = len(partner.instructor_course_ids.filtered(lambda c: c.state not in ['draft','cancelled']))
            