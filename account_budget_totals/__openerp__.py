# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Budget Totals',
    'images': [],
    'summary': """Adds Total fields on Budget form""",
    'author': 'Onestein',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting',
    'version': '8.0.1.0.0',
    'depends': [
        'account_budget',
    ],
    'data': [
        'views/crossovered_budget.xml',
    ],
    'installable': True,
}
