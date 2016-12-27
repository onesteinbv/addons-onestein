# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Activity Based Costing Accessibility",
    'summary': """Activity Based Costing Accessibility""",
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'category': 'Accounting & Finance',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_activity_based_costing',
        'account_analytic_account_accessibility',
        'analytic',
    ],
    'data': [
        'menu_items.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
}
