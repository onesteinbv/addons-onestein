# -*- coding: utf-8 -*-
# Copyright 2015-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    cost_center_id = fields.Many2one(
        'account.cost.center',
        string='Cost Center',
        help='Default Cost Center'
    )

    @api.model
    def line_get_convert(self, line, part):
        res = super(AccountInvoice, self).line_get_convert(line, part)
        if line.get('cost_center_id'):
            res['cost_center_id'] = line['cost_center_id']
        return res

    @api.model
    def invoice_line_move_line_get(self):
        res = super(AccountInvoice, self).invoice_line_move_line_get()

        InvoiceLine = self.env['account.invoice.line']
        for move_line_dict in res:
            line = InvoiceLine.browse(move_line_dict['invl_id'])
            move_line_dict['cost_center_id'] = line.cost_center_id.id

        return res
