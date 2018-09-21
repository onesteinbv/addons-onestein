# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoiceSpreadLine(models.Model):
    _inherit = 'account.invoice.spread.line'

    @api.multi
    def create_move(self):
        self.ensure_one()
        super(AccountInvoiceSpreadLine, self).create_move()
        if self.move_id and self.move_id.state != 'posted':
            self.move_id.post()

    @api.model
    def _create_entries(self):
        lines = super(AccountInvoiceSpreadLine, self)._create_entries()
        for line in lines:
            if line.move_id and line.move_id.state != 'posted':
                line.move_id.post()
        return lines
