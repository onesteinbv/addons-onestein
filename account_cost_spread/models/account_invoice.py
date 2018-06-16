# -*- coding: utf-8 -*-
# Copyright 2014 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_move_create(self):
        """
        When validating an invoice, already create spread lines for each
        invoice line.
        TODO: Isn't this a bit much? Not all invoice lines needs spreading.
        """
        res = super(AccountInvoice, self).action_move_create()
        for this in self:
            for line in this.invoice_line:
                line.compute_spread_board()
        return res

    @api.multi
    def action_cancel(self):
        """ Undo spread when cancelling the invoice """
        for this in self:
            for line in this.invoice_line:
                line.action_undo_spread()
        return super(AccountInvoice, self).action_cancel()
