{
    'name': "Academy Lab",
    'author': "Salma Ameer",
    'category': "",
    'version': "18.0.1.0.0",
    'depends': ['base','mail','contacts','sale','account'],
    'data': [
        'security/academy_security.xml',
        'security/ir.model.access.csv',
        'security/academy_record_rules.xml',

        'views/base_menu.xml',
        'views/course_views.xml',
        'views/category_views.xml',
        'reports/enrollment_report_actions.xml',
        'views/enrollment_views.xml',
        'views/res_partner_views.xml',

        'wizard/sell_course_wizard_view.xml',

        'reports/course_report_actions.xml',
        'reports/course_report_templates.xml',
        'reports/enrollment_report_templates.xml',

    ],
    'application': True, 
}