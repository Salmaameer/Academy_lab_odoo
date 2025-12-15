from odoo import api, models, fields

class CourseCategory(models.Model):
    _name = 'academy.course.category'

    name = fields.Char(required=True)
    description = fields.Text()
    course_ids = fields.One2many(
        'academy.course' , 'category_id' )

    course_count = fields.Integer(
        string = "Number of Courses",
        compute = "_compute_course_count",
        store = True
    )


    @api.depends('course_ids')
    def _compute_course_count(self):
        for cate in self:
            cate.course_count = len(cate.course_ids)   