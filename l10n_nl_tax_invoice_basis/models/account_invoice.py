# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        self.ensure_one()
        move_lines = super(AccountInvoice, self).finalize_invoice_move_lines(
            move_lines
        )
        is_invoice_basis = self.company_id.l10n_nl_tax_invoice_basis
        is_nl = self.company_id.country_id == self.env.ref('base.nl')
        if is_nl and is_invoice_basis:
            for line in move_lines:
                line[2]['l10n_nl_date_invoice'] = self.date_invoice
        return move_lines
