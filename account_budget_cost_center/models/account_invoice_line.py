# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.model
    def _default_cost_center_budget(self):
        return self.env['crossovered.budget'].browse(
            self._context.get('cost_center_budget_id', None))

    cost_center_budget_id = fields.Many2one(
        'crossovered.budget', string='Cost Center Budget',
        domain=[
            ('cost_center_id','!=',False)
        ],
        default=_default_cost_center_budget)

    @api.model
    def move_line_get_item(self, line):
        res = super(AccountInvoiceLine, self).move_line_get_item(line)
        if line.cost_center_budget_id:
            res['cost_center_budget_id'] = line.cost_center_budget_id.id
        return res

    @api.multi
    @api.onchange('cost_center_id')
    def _onchange_cost_center_budget_id(self):
        for line in self:
            if line.cost_center_id:
                if line.cost_center_id != line.cost_center_budget_id.cost_center_id:
                    line.cost_center_budget_id = None
            else:
                line.cost_center_budget_id = None

    @api.multi
    @api.onchange('cost_center_budget_id')
    def _onchange_cost_center_budget_id(self):
        for line in self:
            if line.cost_center_budget_id:
                line.cost_center_id = line.cost_center_budget_id.cost_center_id
