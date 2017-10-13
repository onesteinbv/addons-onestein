# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, SUPERUSER_ID


def migrate(cr, version=None):
    env = api.Environment(cr, SUPERUSER_ID, {})
    account_inv_sl_model = env['account.invoice.spread.line']
    for spreadline in account_inv_sl_model.search([]):
        il_id = spreadline.invoice_line_id
        # check if already reconciled
        has_reconciliation = False
        if len(spreadline.move_id.line_id.mapped('reconcile_id') +
               spreadline.move_id.line_id.mapped('reconcile_partial_id')) > 0:
            has_reconciliation = True
        if (il_id.spread_account_id and
                il_id.spread_account_id.reconcile and
                il_id.spread_account_id == il_id.account_id and
                not has_reconciliation):
            spreadline.move_id.line_id.reconcile()
