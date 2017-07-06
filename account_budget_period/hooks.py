# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID, api, exceptions


def post_init_hook(cr, registry):

    cr.execute(
        'SELECT id, date_from, date_to, company_id FROM crossovered_budget '
        'WHERE date_from IS NOT NULL or date_to IS NOT NULL'
        )
    budget_obj = registry['crossovered.budget']
    period_obj = registry['account.period']
    for budget_data in cr.fetchall():
        period_start = None
        try:
            period_start = budget_data[1] and period_obj.find(
                cr, SUPERUSER_ID,
                budget_data[1],
                context={'company_id': budget_data[3]}
            ) or None
        except exceptions.RedirectWarning:
            pass
        period_stop = None
        try:
            period_stop = budget_data[2] and period_obj.find(
                cr, SUPERUSER_ID,
                budget_data[2],
                context={'company_id': budget_data[3]}
            ) or None
        except exceptions.RedirectWarning:
            pass

        values = {}
        if period_start:
            values['period_start'] = period_start[0]
        if period_stop:
            values['period_stop'] = period_stop[0]

        budget_obj.write(
            cr, SUPERUSER_ID, budget_data[0], values,
            context={'skip_period_date_sync': 1}
        )
