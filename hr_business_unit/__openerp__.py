# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "HR Business Unit",
    'summary': """HR Business Unit""",
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '9.0.1.0.0',
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
