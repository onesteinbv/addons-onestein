{
    'name': 'Calendar Block',
    'category': 'Website',
    'summary': 'Calendar (messaging) on website.',
    'version': '1.0',
    'description': """
        """,
    'author': 'Onestein',
    'depends': ['website', 'calendar', 'web'],
    'data': [
        'views/website_calendar_block.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
    ],
    'installable': True,
}