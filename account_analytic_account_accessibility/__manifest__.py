# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Account Analytic Account Accessibility',
    'summary': 'Improves the Accessibility for the Analytic Account',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting & Finance',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'analytic',
    ],
    'data': [
        'security/res_groups.xml',
        'views/account_analytic_account.xml',
        'menu_items.xml',
    ],
    'installable': True,
}
