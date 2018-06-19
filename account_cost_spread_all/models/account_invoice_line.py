# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.exceptions import ValidationError


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.depends(
        'spread_line_ids.move_id',
        'invoice_id.state',
        'invoice_id.number',
        'spread_line_ids'
    )
    def _compute_display_create_all_moves(self):
        """ Computes 'can_create_move' """
        for line in self:
            line.display_create_all_moves = bool(line.spread_line_ids)
            for spread in line.spread_line_ids:
                try:
                    spread.check_create_move()
                except ValidationError:
                    line.display_create_all_moves = False

    display_create_all_moves = fields.Boolean(
        compute='_compute_display_create_all_moves',
        string='Display Button All Moves')

    @api.multi
    def create_all_moves(self):
        for line in self:
            for spread in line.spread_line_ids:
                spread.check_create_move()
                spread.create_move()
