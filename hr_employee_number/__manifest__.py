# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Employee Number',
    'summary': 'Adds an employee number generated with a sequence',
    'images': [],
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'hr',
    ],
    'data': [
        'data/hr_employee_sequence.xml',
        'views/hr_employee.xml',
    ],
}
