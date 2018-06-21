# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Absence Management in hours',
    'summary': 'Hours based absence notifications',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'images': ['static/description/main_screenshot.png'],
    'category': 'Human Resources',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
        'hr_absenteeism',
        'hr_holidays_hour',
    ],
    'installable': True,
    'auto_install': True,
}
