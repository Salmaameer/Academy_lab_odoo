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
        
        # income_account = self.env['account.account'].search([    ('code', '=', '400000'),    ('company_id', '=', 1)], limit=1)
        # if not income_account:    
        #     # Create income account if it doesn't exist   
        income_account = self.env['account.account'].create({        
            'code': '400000',        
            'name': 'Product Sales',        
            'account_type': 'income', })
             
        product = self.env['product.product'].create({
            'name': self.name,
            'list_price': self.price,
            'type': 'service',
            'course_id': course.id,
            'property_account_income_id': income_account.id if income_account else False,
        })

        # product = self.env['product.product'].create({
        #     'type': 'service',
        #     'name': self.name,
        #     'list_price': self.price,
        #     'course_id': course.id,
            
        # })
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
