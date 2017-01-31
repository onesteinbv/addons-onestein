# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Budget Cost Center',
    'images': [],
    'summary': """Costcenter information for budgets""",
    'author': 'Onestein',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting',
    'version': '8.0.1.0.0',
    'depends': [
        'account_budget',
        'account_cost_center',
        'account_budget_period',
        'account_budget_totals',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crossovered_budget.xml',
        'views/account_cost_center.xml',
        'views/account_invoice.xml',
        'views/account_move.xml',
        'views/account_move_line.xml',
        'reports/account_invoice_report.xml',
        'reports/account_entries_report.xml',
        'reports/account_cost_center_report.xml',
        'views/menus.xml',
    ],
    'installable': True,
}
