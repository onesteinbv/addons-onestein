# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import tools
from openerp import fields, models
import openerp.addons.decimal_precision as dp


class AccountCostCenterReport(models.Model):
    _name = "account.cost.center.report"
    _description = "Cost Center Analysis"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    date = fields.Date('Effective Date', readonly=True)
    date_created = fields.Date('Date Created', readonly=True)
    date_maturity = fields.Date('Date Maturity', readonly=True)
    ref = fields.Char('Reference', readonly=True)
    nbr = fields.Integer('# of Items', readonly=True)
    debit = fields.Float('Debit', readonly=True)
    credit = fields.Float('Credit', readonly=True)
    balance = fields.Float('Balance', readonly=True)
    currency_id = fields.Many2one('res.currency', 'Currency', readonly=True)
    amount_currency = fields.Float('Amount Currency', digits_compute=dp.get_precision('Account'), readonly=True)
    period_id = fields.Many2one('account.period', 'Period', readonly=True)
    account_id = fields.Many2one('account.account', 'Account', readonly=True)
    journal_id = fields.Many2one('account.journal', 'Journal', readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    product_uom_id = fields.Many2one('product.uom', 'Product Unit of Measure', readonly=True)
    move_state = fields.Selection([
        ('draft','Unposted'),
        ('posted','Posted')
    ], 'Status', readonly=True)
    move_line_state = fields.Selection([('draft','Unbalanced'), ('valid','Valid')], 'State of Move Line', readonly=True)
    reconcile_id = fields.Many2one('account.move.reconcile', 'Reconciliation number', readonly=True)
    partner_id = fields.Many2one('res.partner','Partner', readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True)
    quantity = fields.Float('Products Quantity', digits=(16,2), readonly=True)
    user_type = fields.Many2one('account.account.type', 'Account Type', readonly=True)
    type = fields.Selection([
        ('receivable', 'Receivable'),
        ('payable', 'Payable'),
        ('cash', 'Cash'),
        ('view', 'View'),
        ('consolidation', 'Consolidation'),
        ('other', 'Regular'),
        ('closed', 'Closed'),
    ], 'Internal Type', readonly=True, help="This type is used to differentiate types with "\
        "special effects in Odoo: view can not have entries, consolidation are accounts that "\
        "can have children accounts for multi-company consolidations, payable/receivable are for "\
        "partners accounts (for debit/credit computations), closed for depreciated accounts.")
    company_id = fields.Many2one('res.company', 'Company', readonly=True)

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
        digits=dp.get_precision('Account')
    )
    amount_planned = fields.Float(
        string='Planned amount',
        digits=dp.get_precision('Account')
    )

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
            context=None, count=False):
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        period_obj = self.pool.get('account.period')
        for arg in args:
            if arg[0] == 'period_id' and arg[2] == 'current_period':
                current_period = period_obj.find(cr, uid, context=context)[0]
                args.append(['period_id','in',[current_period]])
                break
            elif arg[0] == 'period_id' and arg[2] == 'current_year':
                current_year = fiscalyear_obj.find(cr, uid)
                ids = fiscalyear_obj.read(cr, uid, [current_year], ['period_ids'])[0]['period_ids']
                args.append(['period_id','in',ids])
        for a in [['period_id','in','current_year'], ['period_id','in','current_period']]:
            if a in args:
                args.remove(a)
        return super(AccountCostCenterReport, self).search(cr, uid, args=args, offset=offset, limit=limit, order=order,
            context=context, count=count)

    def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False,lazy=True):
        if context is None:
            context = {}
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        period_obj = self.pool.get('account.period')
        if context.get('period', False) == 'current_period':
            current_period = period_obj.find(cr, uid, context=context)[0]
            domain.append(['period_id','in',[current_period]])
        elif context.get('year', False) == 'current_year':
            current_year = fiscalyear_obj.find(cr, uid)
            ids = fiscalyear_obj.read(cr, uid, [current_year], ['period_ids'])[0]['period_ids']
            domain.append(['period_id','in',ids])
        else:
            domain = domain
        return super(AccountCostCenterReport, self).read_group(cr, uid, domain, fields, groupby, offset, limit, context, orderby,lazy)

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'account_cost_center_report')
        cr.execute("""
            create or replace view account_cost_center_report as (
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
                and l.cost_center_budget_id is not null
            )
        """)
