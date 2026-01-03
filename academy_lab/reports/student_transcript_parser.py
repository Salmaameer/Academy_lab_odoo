from odoo import models, api
from datetime import datetime

class StudentTranscript(models.AbstractModel):
    _name = "report.academy_lab.report_student_transcript_template"
    _description = "Student Transcript Report Parser"

    @api.model
    def _get_report_values(self, docids, data=None):

        students = self.env["res.partner"].browse(docids)


        transcript_data = []

        # get all student's enrolls
        for stud in students:
            #all enrolls no restrict on the state 
            enrolls = self.env['academy.enrollment'].search([
                ('student_id','=', stud.id)
            ]) 

            # get all grades
            grades = enrolls.mapped('grade')
            grades = [g for g in grades if g is not None]

            #compute the statistics 
            total_courses = len(enrolls)
            avrg_grade = 0.0
            if grades:
                avrg_grade = sum(grades) / len(grades) 

            # top grade 3 courses
            top_courses = enrolls.sorted(
                key=lambda e: e.grade or 0,
                reverse=True
            )[0:3] 

            transcript_data.append({
                'student':stud,
                'enrollments': enrolls,
                'avg_grade': round(avrg_grade,2),
                'total_courses': total_courses,
                'top_courses': top_courses,
            })  

        return{
            'doc_ids':docids,
            'doc_model':'res.partner',
            'docs': students,
            'report_date': datetime.now(),
            'report_data':transcript_data,
        }


        

