# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def name_get(self):
        res = super(AccountAnalyticAccount, self).name_get()
        new_list = []
        for item in res:
            if item and item[1]:
                Account = self.env['account.analytic.account']
                company = Account.browse(item[0]).company_id
                company_name = company and company.name or ''
                fullname = item[1] + ' - ' + company_name
                new_list.append((item[0], fullname))
        return new_list
