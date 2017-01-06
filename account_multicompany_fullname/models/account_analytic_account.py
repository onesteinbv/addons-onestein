# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.model
    def _fullname_get(self, item):
        name = item[1] or ''
        Account = self.env['account.analytic.account']
        company = Account.browse(item[0]).company_id
        company_name = company and company.name or ''
        return name + ' - ' + company_name

    @api.multi
    def name_get(self):
        res = super(AccountAnalyticAccount, self).name_get()
        new_list = []
        for item in res:
            fullname = self._fullname_get(item)
            new_list.append((item[0], fullname))
        return new_list
