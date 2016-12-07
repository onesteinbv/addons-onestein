# -*- coding: utf-8 -*-
# Copyright 2015 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.model
    def _default_cost_center(self):
        return self.env['account.cost.center'].browse(
            self._context.get('cost_center_id', None))

    cost_center_id = fields.Many2one(
        'account.cost.center', string='Cost Center',
        default=_default_cost_center)

    @api.model
    def move_line_get_item(self):
        res = super(AccountInvoiceLine, self).invoice_line_move_line_get()

        InvoiceLine = self.env['account.invoice.line']
        for move_line_dict in res:
            line = InvoiceLine.browse(move_line_dict['invl_id'])
            move_line_dict['cost_center_id'] = line.cost_center_id.id

        return res
