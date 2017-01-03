# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)from openerp import api, fields, models

from openerp import models, fields, api, _


class AccountingReport(models.TransientModel):

    _inherit = "accounting.report"

    cost_center_ids = fields.Many2many(
            comodel_name='account.cost.center',
            string='Cost Centers',
    )

    @api.multi
    def _build_contexts(self, data):
        result = super(AccountingReport, self)._build_contexts(data)
        data2 = {}
        data2['form'] = self.read(['cost_center_ids'])[0]
        result['cost_center_ids'] = 'cost_center_ids' in data2['form']\
                                       and data2['form']['cost_center_ids']\
                                       or False
        return result

    @api.multi
    def _build_comparison_context(self, data):
        result = super(AccountingReport, self)._build_comparison_context(data)
        data['form'] = self.read(['cost_center_ids'])[0]
        result['cost_center_ids'] = 'cost_center_ids' in data['form'] \
                                       and data['form']['cost_center_ids'] \
                                       or False
        return result
