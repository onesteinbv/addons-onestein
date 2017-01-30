# -*- coding: utf-8 -*-
# Copyright 2015 Anubía, soluciones en la nube,SL (http://www.anubia.es)
# Copyright 2017 Onestein (http://www.onestein.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.multi
    def name_get(self):

        def _fullname_get(item, company):
            name = item[1] or ''
            company_name = company and company.name or ''
            return name + ' - ' + company_name

        res = super(Base, self).name_get()
        if self._name in ['account.account',
                          'account.analytic.account',
                          'account.fiscal.position',
                          'account.journal',
                          'account.tax']:
            list = []
            for item in res:
                company = self.browse(item[0]).company_id
                fullname = _fullname_get(item, company)

                list.append((item[0], fullname))
            return list
        return res
