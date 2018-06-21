# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Absence Management',
    'summary': 'Create time based absence notifications',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'images': ['static/description/main_screenshot.png'],
    'category': 'Human Resources',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_holidays_status.xml',
        'views/hr_holidays.xml',
        'data/hr_absenteeism_cron.xml',
    ],
    'installable': True,
}
