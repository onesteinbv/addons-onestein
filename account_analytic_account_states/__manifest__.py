# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Account Analytic Account State',
    'summary': 'Workflow for the analytic accounts',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting & Finance',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'analytic',
        'account_analytic_account_accessibility',
        'project',
    ],
    'data': [
        'security/account_analytic_account_security.xml',
        'views/account_analytic_account.xml',
        'wizards/account_analytic_account_approve.xml',
        'data/analytic_account_data.xml',
    ],
    'installable': True,
}
