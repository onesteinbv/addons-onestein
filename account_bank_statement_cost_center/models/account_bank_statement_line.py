# -*- coding: utf-8 -*-
# Copyright (c) 2009-2016 Noviat nv/sa (www.noviat.com)
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import api, fields, models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    @api.model
    def _default_cost_center(self):
        return self.env['account.cost.center'].browse(
                self._context.get('cost_center_id', None))

    cost_center_id = fields.Many2one(
            comodel_name='account.cost.center',
            string='Cost Center',
            default=_default_cost_center
    )

    @api.model
    def get_statement_line_for_reconciliation(self, st_line):
        data = super(AccountBankStatementLine, self).\
            get_statement_line_for_reconciliation(st_line)
        data['cost_center_id'] = st_line.cost_center_id.id
        return data
