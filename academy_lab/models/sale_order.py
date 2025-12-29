from odoo import models



class SaleOrder(models.Model):
    _inherit = 'sale.order'


    import logging
    _logger = logging.getLogger(__name__)

    def  action_confirm(self):

        res = super(SaleOrder,self).action_confirm()
        print("action confirm triggered")

        for order in self:
            # if not order.invoice_ids:
            #     order._create_invoices()

            for line in order.order_line:
                product = line.product_id

                if not product.course_id:
                    raise ValidationError("The product on the order line is not linked to a course.")

                   
                course = product.course_id
                student = order.partner_id

                #check no duplicate enrollments
                enrollmntExist = self.env['academy.enrollment'].search([
                    ('student_id', '=' ,student.id),
                    ('course_id', '=' ,course.id),

                ], limit = 1)

                if enrollmntExist:
                    continue
                
                #create the new enrollment
                self.env['academy.enrollment'].create({
                    'student_id' : student.id,
                    'course_id'  : course.id,
                    'state'      : 'draft',
                })

        return res

                


