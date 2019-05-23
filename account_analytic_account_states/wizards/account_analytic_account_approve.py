# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountAnalyticAccountApprove(models.TransientModel):
    _name = "account.analytic.account.approve"
    _description = "Wizard - Approve analytic accounts"

    @api.multi
    def approve_analytic_accounts(self):
        self.ensure_one()
        AnalyticAccount = self.env['account.analytic.account']
        accounts = AnalyticAccount.browse(self._context.get('active_ids'))
        accounts.action_approve()
