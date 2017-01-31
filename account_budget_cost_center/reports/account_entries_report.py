# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import tools
from openerp import fields, models
import openerp.addons.decimal_precision as dp


class AccountEntriesReport(models.Model):
    _inherit = "account.entries.report"

    cost_center_id = fields.Many2one(
        'account.cost.center',
        string="Cost Center",
        readonly=True
    )
    cost_center_budget_id = fields.Many2one(
        'crossovered.budget',
        string="Cost Center Budget",
        domain=[
            ('cost_center_id','!=',False)
        ],
        readonly=True
    )
    forecast = fields.Float(
        digits=dp.get_precision('Account'),
        readonly=True
    )
    amount_planned = fields.Float(
        string='Planned amount',
        digits=dp.get_precision('Account'),
        readonly=True
    )

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'account_entries_report')
        cr.execute("""
            create or replace view account_entries_report as (
            select
                l.id as id,
                am.date as date,
                l.date_maturity as date_maturity,
                l.date_created as date_created,
                am.ref as ref,
                am.state as move_state,
                l.state as move_line_state,
                l.reconcile_id as reconcile_id,
                l.partner_id as partner_id,
                l.product_id as product_id,
                l.product_uom_id as product_uom_id,
                am.company_id as company_id,
                am.journal_id as journal_id,
                p.fiscalyear_id as fiscalyear_id,
                am.period_id as period_id,
                l.account_id as account_id,
                l.analytic_account_id as analytic_account_id,
                a.type as type,
                a.user_type as user_type,
                1 as nbr,
                l.quantity as quantity,
                l.currency_id as currency_id,
                l.amount_currency as amount_currency,
                l.debit as debit,
                l.credit as credit,
                l.cost_center_id as cost_center_id,
                l.cost_center_budget_id as cost_center_budget_id,
                cb.forecast as forecast,
                cb.amount_planned as amount_planned,
                coalesce(l.debit, 0.0) - coalesce(l.credit, 0.0) as balance
            from
                account_move_line l
                left join account_account a on (l.account_id = a.id)
                left join account_move am on (am.id=l.move_id)
                left join account_period p on (am.period_id=p.id)
                left join crossovered_budget cb on (l.cost_center_budget_id=cb.id)
                where l.state != 'draft'
            )
        """)
