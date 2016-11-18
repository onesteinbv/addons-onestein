# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _


class AccountBudgetPost(models.Model):
    _inherit = "account.budget.post"

    @api.multi
    @api.depends('account_ids')
    def _get_account_id(self):
        for bp in self:
            bp.account_id = bp.account_ids and bp.account_ids[0] or None

    @api.multi
    @api.depends('account_id')
    def _set_account_id(self):
        for bp in self:
            if bp.account_id:
                bp.account_ids = bp.account_id
            else:
                bp.account_ids = None

    account_id = fields.Many2one(
        compute='_get_account_id',
        inverse ='_set_account_id',
        comodel_name='account.account',
        string='Account',
        store=True
    )

    @api.model
    def create(self, vals):
        account_id = vals.get('account_id')
        if account_id:
            vals['account_ids'] = [(4, account_id)]

        return super(AccountBudgetPost, self).create(vals)
