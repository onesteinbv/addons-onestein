# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    @api.multi
    def _get_running_state(self):
        today = fields.Date.today()
        state = ''
        for budget in self:
            if budget.state == 'cancel':
                state = 'cancel'
            elif budget.date_from <= today and budget.date_to >= today:
                state = 'running'
            elif budget.date_from > today:
                state = 'draft'
            elif budget.date_to < today:
                state = 'done'
            budget.running_state = state

    creating_user_id = fields.Many2one(
        string='Responsible'
    )
    cost_center_id = fields.Many2one(
        'account.cost.center',
        string='Cost Center'
    )
    running_state = fields.Selection(
        compute='_get_running_state',
        selection=[
            ('draft', 'Draft'),
            ('running', 'Running'),
            ('cancel', 'Cancelled'),
            ('done', 'Done')
        ],
        string='Running Status')

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if args is None:
            args = []
        if context is None:
            context = {}
        if context.get('enable_cost_center'):
            args += [('cost_center_id','!=',False)]
        date = context.get('filter_invoice_date')
        period_id = context.get('filter_invoice_period')
        if period_id:
            period_obj = self.pool.get('account.period')
            period = period_obj.browse(cr, uid, period_id)
            args += [('date_from','<=',period.date_stop)]
            args += [('date_to','>=',period.date_start)]
        elif date:
            args += [('date_from','<=',date)]
            args += [('date_to','>=',date)]

        return super(CrossoveredBudget, self).name_search(
            cr, uid, name, args=args, operator=operator,
            context=context, limit=limit)
