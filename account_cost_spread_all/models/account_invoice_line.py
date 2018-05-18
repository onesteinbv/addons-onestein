# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def _display_create_all_moves(self):
        for line in self:
            line.display_create_all_moves = False
            for spread in line.spread_line_ids:
                if not spread.move_id \
                        and not spread.init_entry \
                        and not spread.move_check \
                        and spread.can_create_move:
                    line.display_create_all_moves = True
                    break

    display_create_all_moves = fields.Boolean(
        compute='_display_create_all_moves',
        string='Display Button All Moves')

    @api.multi
    def create_all_moves(self):
        for line in self:
            for spread in line.spread_line_ids:
                if not spread.move_id \
                        and not spread.init_entry \
                        and not spread.move_check \
                        and spread.can_create_move:
                    spread.create_move()
