# -*- coding: utf-8 -*-
{
    'name': 'demo Hospital Management',
    'version': '1.0',
    'summary': 'Hospital Management Software',
    'sequence': -100,
    'description': """Hospital Management Software""",
    'category': 'Productivity',

    'license': 'LGPL-3',
    'depends': ['mail'],
    'data': [
          'security/ir.model.access.csv',
          'view/patient.xml',
           'data/sequence.xml',
           'view/appointment.xml',
        'view/hospital_security.xml',
                'view/doctor.xml',
        'view/hospital_dashbord.xml',
'view/HospitalRoom.xml',
'view/rooom.xml',
'view/hospital_lab_request.xml',
'view/hospital_lab_test.xml',
        'report/report_hospital_lab_test.xml',




    ],
'qweb': [
        'static/src/xml/*.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hopital/static/src/css/hospital_patient_styles.css',
            'hopital/static/src/css/dashboard.css',
            'hopital/static/src/css/room.css',
            # Add other CSS or JS files here if needed
        ],},
'images': ['static/src/description/icon.png'],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}