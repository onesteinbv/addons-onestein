# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Employee Relatives",
    'images': ['static/description/main_screenshot.png'],
    'summary': """Store employee relatives for communication.""",
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_related.xml',
        'views/hr_employee.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
