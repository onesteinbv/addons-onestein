# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Account Analytic Account State",
    'summary': """Account Analytic Account State""",
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting & Finance',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'analytic',
        'account_analytic_account_accessibility',
        'project',
    ],
    'data': [
        'security/account_analytic_account_security.xml',
        'views/account_analytic_account.xml',
        'wizard/account_analytic_account_approve.xml',
        'data/analytic_account_data.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
