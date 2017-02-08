# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "HR Business Unit",
    'images': [],
    'summary': """HR Business Unit""",
    'author': "Onestein",
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '8.0.1.0.0',
    'depends': [
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
