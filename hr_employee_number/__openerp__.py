# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Employee Number",
    'summary': """Adds an employee number generated with a sequence""",
    'images': [],
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '1.2',
    'depends': [
        'hr',
    ],
    'data': [
        'data/hr_employee_sequence.xml',
        'views/hr_employee.xml',
    ],
}
