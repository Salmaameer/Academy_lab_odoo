from odoo import models, fields, _
from odoo.exceptions import UserError


class PrintEnrollmentReportWizard(models.TransientModel):
    _name = "academy.print.wizard"

    
    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    student_name = fields.Many2one("res.partner", string="Student Name", required=True)

    

    def action_apply_filter(self):
        self.ensure_one()

        domain = [
            ('enrollment_date', '>=', self.from_date),
            ('enrollment_date', '<=', self.to_date),
            ("student_id" ,'=' ,self.student_name.id)

        ]
      
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
