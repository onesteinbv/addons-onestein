# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Public Holidays Leaves",
    'images': [],
    'summary': """Leaves management for public holidays""",
    'author': "ONESTEiN BV",
    'license': 'AGPL-3',
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '9.0.1.0.0',
    'depends': [
        'hr_holidays',
        'hr_public_holidays',
    ],
    'data': [
        'security/hr_public_holiday_security.xml',
        'data/hr_holidays_status.xml',
        'views/hr_public_holiday.xml',
        'menu_items.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
