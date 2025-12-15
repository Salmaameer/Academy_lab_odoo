{
    'name': "Academy Lab",
    'author': "Salma Ameer",
    'category': "",
    'version': "18.0.1.0.0",
    'depends': ['base', 'mail' , 'contacts'],
    'data': [
        'security/academy_security.xml',
        'security/ir.model.access.csv',
        'security/academy_record_rules.xml',
        'views/base_menu.xml',
        'views/course_views.xml',
        'views/category_views.xml',
        'views/enrollment_views.xml',

    ],
    'application': True,          

}