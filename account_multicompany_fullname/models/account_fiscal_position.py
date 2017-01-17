# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    @api.model
    def _fullname_get(self, item):
        name = item[1] or ''
        FiscalPosition = self.env['account.fiscal.position']
        company = FiscalPosition.browse(item[0]).company_id
        company_name = company and company.name or ''
        return name + ' - ' + company_name

    @api.multi
    def name_get(self):
        res = super(AccountFiscalPosition, self).name_get()
        fp_list = []
        for item in res:
            fullname = self._fullname_get(item)
            fp_list.append((item[0], fullname))
        return fp_list
