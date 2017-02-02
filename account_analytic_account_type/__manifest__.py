# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Account Analytic Account Type",
    'summary': """Adds a Type field in the Analytic Account""",
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting & Finance',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'analytic',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_analytic_account.xml',
        'views/account_analytic_type.xml',
        'menu_items.xml',
    ],
    'demo': [],
}
