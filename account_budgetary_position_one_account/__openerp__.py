# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Budgetary Position One Account',
    'images': [],
    'summary': """Select only one Account in Budgetary Positions""",
    'author': 'Onestein',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting',
    'version': '8.0.1.0.0',
    'depends': [
        'account_budget',
    ],
    'data': [
        'views/account_budget_post.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
}
