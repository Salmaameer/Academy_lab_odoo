from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    course_id = fields.Many2one('academy.course')
