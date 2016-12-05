# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    @api.multi
    @api.depends('crossovered_budget_line', 'crossovered_budget_line.practical_amount', 'crossovered_budget_line.planned_amount')
    def _get_amounts(self):
        for budget in self:
            amount_practical = 0.0
            amount_planned = 0.0
            for line in budget.crossovered_budget_line:
                amount_practical += line.practical_amount
                amount_planned += line.planned_amount
            budget.amount_practical = amount_practical
            budget.amount_planned = amount_planned
            budget.amount_practical_perc = 0.0
            if amount_planned:
                perc = float((amount_practical or 0.0) / amount_planned) * 100
                budget.amount_practical_perc = perc

    amount_planned = fields.Float(
        compute='_get_amounts',
        string='Planned amount',
        store=True,
        digits=dp.get_precision('Account')
    )
    amount_practical = fields.Float(
        compute='_get_amounts',
        string='Practical amount',
        store=False,
        digits=dp.get_precision('Account')
    )
    amount_practical_perc = fields.Float(
        compute='_get_amounts',
        store=True,
        string='% practical/planned'
    )
    forecast = fields.Float(
        'Forecast',
        digits=dp.get_precision('Account')
    )
