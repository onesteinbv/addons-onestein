# -*- coding: utf-8 -*-
# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Cost Spread - All moves in one click',
    'summary': 'Create all the moves for Cost spreading in just one click',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
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
