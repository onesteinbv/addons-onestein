# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID, api


def post_init_hook(cr, registry):

    cr.execute(
        'SELECT budget_id, min(account_id) as account_id FROM account_budget_rel '
        'GROUP BY budget_id'
        )
    budget_post_obj = registry['account.budget.post']

    for budget_data in cr.fetchall():
        budget_post_obj.write(
            cr, SUPERUSER_ID, budget_data[0],
            {'account_id': budget_data[1]
             }
        )
