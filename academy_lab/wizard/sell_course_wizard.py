from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class SellCourse(models.TransientModel):
    _name = "academy.product.wizard"
    _description = "Course Sale Wizard"

    name = fields.Char(required=True)
    price = fields.Float(required=True)


    def action_create(self):
        self.ensure_one()

        course_id = self.env.context.get('active_id')
        if not course_id:
            raise ValidationError("No course found in context!")

        course = self.env['academy.course'].browse(course_id)

        if not course.exists():
            raise ValidationError("The course record no longer exists.")
        
        if self.price <= 0 :
            raise ValidationError("Course price must be greater than 0")

        product = self.env['product.product'].create({
            'name': self.name,
            'list_price': self.price,
            'type': 'service',
            'course_id': course.id,
        })

        
        _logger.info("Product created %s", product.name)

        course.product_id = product.id

        #create the sale order 
        self.env['sale.order'].create({
            'partner_id': self.env.user.partner_id.id,
            'order_line': [(0, 0, {
                'product_id': product.id,
                'product_uom_qty': 1,
                'price_unit': self.price,
            })],
        })

        return {'type': 'ir.actions.act_window_close'}
