{
    'name': 'Office 365 Connector - Leaves',
    'summary': 'Push HR Leaves to Office 365',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'website': 'https://github.com/onesteinbv/addons-onestein/',
    'category': 'Tools',
    'version': '12.0.1.0.0',
    'development_status': 'Alpha',
    'depends': [
        'connector_office_365',
        'hr_holidays',
    ],
    'external_dependencies': {
        #only needed for tests
        'python': ['responses']
    },
    'data': [
        'data/mail_template.xml',
        'views/hr_leave_views.xml',
    ],
    'images': [
        'static/description/cover.png'
    ]
}
