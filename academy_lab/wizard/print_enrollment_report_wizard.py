from odoo import models, fields, _,api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class PrintEnrollmentReportWizard(models.TransientModel):
    _name = "academy.print.wizard"

    #common fields
    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)

    
    student_name = fields.Many2one("res.partner", string="Student Name")
    course_name = fields.Many2one('academy.course')

    filter_by = fields.Selection(
        [("enrollment","Enrollment"),
         ("course", "Course")],
         readonly = True,
         default = lambda self: self.env.context["filter_by"])

    def action_apply_filter(self):
        self.ensure_one()
        filter_by = self.env.context.get('filter_by')
        active_id = self.env.context.get('active_id')

        _logger.info("filter by is: %s",filter_by)
        domain = [
            ('enrollment_date', '>=', self.from_date),
            ('enrollment_date', '<=', self.to_date),
        ]

        # if filter_by == "course":
        #     domain.append(('course_id','=',active_id))

        if filter_by == "enrollment":
            domain.append(('course_id','=',self.course_name.id))    
      
        # search for the filter enrolls
        enrolls_found = self.env["academy.enrollment"].search(domain)

        if not enrolls_found:
            raise UserError(
                _("No enrolls found for the given data"))


        return{
            "type":"ir.actions.act_window",
            "name": "Filltered Enrollments",
            "res_model": 'academy.enrollment',
            "domain": domain,
            "target":"current",
            "view_mode":"list,form",

        }
