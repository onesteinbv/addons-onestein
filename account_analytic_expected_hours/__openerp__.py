# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Account Analytic Expected Hours",
    'images': [],
    'summary': """Block writing hours on reaching expected hours""",
    'author': 'Onestein',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'category': 'Sales Management',
    'version': '8.0.1.0.0',
    'depends': [
        'account_analytic_analysis',
    ],
    'data': [
        'views/account_analytic_account.xml',
        'views/hr_analytic_timesheet.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
