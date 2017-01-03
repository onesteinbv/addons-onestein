# -*- coding: utf-8 -*-
# Copyright (c) 2009-2016 Noviat nv/sa (www.noviat.com)
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import api, models, _
from openerp.addons.report_xls.utils import _render


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def _report_xls_fields(self):
        res = super(AccountMoveLine, self)._report_xls_fields()
        ix = res.index('account')
        res.insert(ix + 1, 'cost_center_name')
        return res

    @api.model
    def _report_xls_template(self):
        update = super(AccountMoveLine, self).\
            _report_xls_template()
        update['cost_center_name'] = {
            'header': [1, 25, 'text', _('Cost Center')],
            'lines': [
                1, 0, 'text', _render(
                    "line.cost_center_id and "
                    "line.cost_center_id.name "
                    "or ''")],
            'totals': [1, 0, 'text', None]}
        return update
