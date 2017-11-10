# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang
from odoo.exceptions import Warning as UserError


OMZET_DISPLAY = (
    '1a', '1b', '1c', '1d', '1e',
    '2a',
    '3a', '3b', '3c',
    '4a', '4b'
)

BTW_DISPLAY = (
    '1a', '1b', '1c', '1d',
    '2a',
    '4a', '4b',
    '5a', '5b', '5c', '5d', '5e', '5f'
)

GROUP_DISPLAY = (
    '1', '2', '3', '4', '5'
)

EDITABLE_DISPLAY = (
    '5d', '5e', '5f'
)


class VatStatementLine(models.Model):
    _name = 'l10n.nl.vat.statement.line'
    _order = 'code'

    name = fields.Char()
    code = fields.Char()

    statement_id = fields.Many2one(
        'l10n.nl.vat.statement',
        'Statement'
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='statement_id.company_id.currency_id',
        readonly=True,
        help='Utility field to express amount currency'
    )
    omzet = fields.Monetary()
    btw = fields.Monetary()
    format_omzet = fields.Char(compute='_compute_amount_format')
    format_btw = fields.Char(compute='_compute_amount_format')

    is_group = fields.Boolean(compute='_compute_is_group')
    is_readonly = fields.Boolean(compute='_compute_is_readonly')

    state = fields.Selection(related='statement_id.state')

    @api.multi
    @api.depends('omzet', 'btw', 'code')
    def _compute_amount_format(self):
        for line in self:
            omzet = formatLang(self.env, line.omzet, monetary=True)
            btw = formatLang(self.env, line.btw, monetary=True)
            if line.code in OMZET_DISPLAY:
                line.format_omzet = omzet
            if line.code in BTW_DISPLAY:
                line.format_btw = btw

    @api.multi
    @api.depends('code')
    def _compute_is_group(self):
        for line in self:
            line.is_group = line.code in GROUP_DISPLAY

    @api.multi
    @api.depends('code')
    def _compute_is_readonly(self):
        for line in self:
            if line.state == 'draft':
                line.is_readonly = line.code not in EDITABLE_DISPLAY
            else:
                line.is_readonly = True

    @api.multi
    def unlink(self):
        for line in self:
            if line.statement_id.state == 'posted':
                raise UserError(
                    _('You cannot delete lines of a posted statement! '
                      'Reset the statement to draft first.'))
            if line.statement_id.state == 'final':
                raise UserError(
                    _('You cannot delete lines of a statement set as final!'))
        super(VatStatementLine, self).unlink()
