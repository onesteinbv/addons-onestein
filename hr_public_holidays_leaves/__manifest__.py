# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Public Holidays Leaves",
    'images': [],
    'summary': """Leaves management for public holidays""",
    'author': "Onestein",
    'license': 'AGPL-3',
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'depends': [
        'hr_holidays',
        'hr_public_holidays',
    ],
    'data': [
        'security/hr_public_holiday_security.xml',
        'data/hr_holidays_status.xml',
        'views/hr_public_holiday.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
