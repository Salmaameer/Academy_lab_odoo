from odoo import models 
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super().action_post()

        for move in self:

            for line in move.invoice_line_ids:
                product = line.product_id
                if not product or not product.course_id:
                    continue

                course = product.course_id
                student = move.partner_id

                #check no duplicate enrollments
                enrollmnt = self.env['academy.enrollment'].search([
                    ('student_id', '=' ,student.id),
                    ('course_id', '=' ,course.id),

                ], limit=1)

                if not enrollmnt:
                    raise ValidationError(
                        f"No enrollment found for {student.name} in course {course.name}"
                    )

                #update the enrollment state
                enrollmnt.write({
                    'state':'confirmed',
                    'invoice_id': move.id
                })

        return res


