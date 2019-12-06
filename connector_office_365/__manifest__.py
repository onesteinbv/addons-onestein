{
    'name': 'Office 365 Connector',
    'summary': 'Sync your Office 365 calendar with Odoo',
    'author': 'Onestein',
    'license': 'AGPL-3',
    'website': 'https://www.onestein.nl',
    'category': 'Tools',
    'version': '12.0.1.0.2',
    'development_status': 'Alpha',
    'depends': [
        'calendar'
    ],
    'external_dependencies': {
        'python': ['requests_oauthlib']
    },
    'data': [
        'templates/assets.xml',
        'views/res_config_settings_view.xml',
        'views/calendar_event_view.xml'
    ],
    'qweb': [
        'static/src/xml/backend.xml'
    ],
    'images': [
        'static/description/cover.png'
    ]
}
