# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import Warning


class AccountCostCenter(models.Model):
    _inherit = 'account.cost.center'

    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')
    budget_ids = fields.One2many(
        comodel_name='crossovered.budget',
        inverse_name='cost_center_id',
        string='Budgets'
    )

    @api.model
    def create(self, vals):
        if vals.get('date_start') and vals.get('date_end'):
            date_start = vals.get('date_start')
            date_end = vals.get('date_end')
            warning = _('End date can never be earlier than start date!')
            if date_end < date_start:
                raise Warning(warning)
        return super(AccountCostCenter, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'date_start' in vals:
            date_start = None
            if vals.get('date_start'):
                date_start = vals.get('date_start')
        if 'date_end' in vals:
            date_end = None
            if vals.get('date_end'):
                date_end = vals.get('date_end')

        for costcenter in self:
            if 'date_start' not in vals:
                date_start = costcenter.date_start
            if 'date_end' not in vals:
                date_end = costcenter.date_end

            if date_start and date_end:
                warning = _('End date can never be earlier than start date!')
                if date_end < date_start:
                    raise Warning(warning)

        return super(AccountCostCenter, self).write(vals)
