# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID


def post_init_hook(cr, registry):

    cr.execute(
        'SELECT id, date_from, date_to, company_id '
        'FROM crossovered_budget_lines '
        'WHERE date_from IS NOT NULL or date_to IS NOT NULL'
        )
    budget_lines_obj = registry['crossovered.budget.lines']
    period_obj = registry['account.period']
    for line_data in cr.fetchall():
        period_start = line_data[1] and period_obj.find(
            cr, SUPERUSER_ID,
            line_data[1],
            context={'company_id': line_data[3]}
        ) or None
        period_stop = line_data[2] and period_obj.find(
            cr, SUPERUSER_ID,
            line_data[2],
            context={'company_id': line_data[3]}
        ) or None

        budget_lines_obj.write(
            cr, SUPERUSER_ID, line_data[0],
            {'period_start': period_start and period_start[0] or None,
             'period_stop': period_stop and period_stop[0] or None
             },
            context={'skip_period_date_sync': 1}
        )
