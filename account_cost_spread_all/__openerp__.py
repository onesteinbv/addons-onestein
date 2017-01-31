# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Cost / Income Spread - All moves in one click',
    'summary': """Create all the moves for Cost and Income spreading in just one click""",
    'version': '1.0',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting',
    'depends': [
        'account_cost_spread',
    ],
    'data': [
        'views/account_invoice_line_view.xml',
    ],
}
