{
    'name': 'Leave Signature',
    'version': '1.1',
    'sequence': 150,
    'category': 'Human Resources',
    'summary': '',
    'description': """
""",
    'author': 'ONESTEiN BV',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'depends': ['hr_holidays', 'web_draw'],
    'data': [
        'views/hr_holidays_signature.xml'
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
