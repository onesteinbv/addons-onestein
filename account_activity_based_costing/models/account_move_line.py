# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # THIS METHOD IS NEEDED BECAUSE THE ANALYTIC LINE ARE DELETED
    # THROUGH AN ON DELETE CASCADE WHEN THE RELATED ACCOUNT
    # MOVE IS DELETED. THIS DOESN'T TRIGGER THE _get_realized_data()
    # METHOD TO RECOMPUTE FIELDS DEPENDING ON ANALYTIC LINES
    @api.multi
    def unlink(self):
        accounts = []
        for line in self:
            if line.analytic_account_id:
                if line.analytic_account_id.id not in accounts:
                    accounts.append(line.analytic_account_id.id)
        res = super(AccountMoveLine, self).unlink()
        AnalyticAccount = self.env['account.analytic.account']
        AnalyticAccount.browse(accounts)._get_realized_data()
        return res
