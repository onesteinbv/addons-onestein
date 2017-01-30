# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Leave Hours",
    'summary': """Leave Request in Hours""",
    'author': "Onestein",
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
        'hr_contract',
        'hr_employee_holidays',
        'hr_holidays_expiration',  # for approval_date
        'hr_contract_accessibility',  # for access rules on contracts
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'views/hr_holidays.xml',
        'views/hr_holidays_status.xml',
        'report/hr_holidays_report_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
