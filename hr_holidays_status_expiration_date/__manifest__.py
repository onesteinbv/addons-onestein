# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'HR Holidays Type Expiration Date',
    'summary': '''HR Holidays Type Sort''',
    'author': 'ONESTEiN BV',
    'website': 'http://www.onestein.eu',
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'depends': [
        'hr_holidays',
        'hr_leave_hours',
    ],
    'data': [
        'views/hr_holidays_status.xml',
    ],
    'installable': True,
}
