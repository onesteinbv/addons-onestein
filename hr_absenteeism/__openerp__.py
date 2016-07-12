# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Absence Management",
    'summary': """Create time based absence notifications""",
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'images': ['static/description/main_screenshot.png'],
    'category': 'Human Resources',
    'version': '9.0.1.0.0',
    'depends': [
        'hr_holidays',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_holidays_status.xml',
        'data/hr_absenteeism_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
