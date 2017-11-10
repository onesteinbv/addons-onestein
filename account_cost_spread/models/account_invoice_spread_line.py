# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

import odoo.addons.decimal_precision as dp
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class AccountInvoiceSpreadLine(models.Model):
    _name = 'account.invoice.spread.line'
    _description = 'Account Invoice Spread Lines'

    _order = 'type, line_date'

    name = fields.Char('Spread Name', size=64, readonly=True)
    invoice_line_id = fields.Many2one(
        comodel_name='account.invoice.line',
        string='Invoice Line',
        required=True)
    previous_id = fields.Many2one(
        comodel_name='account.invoice.spread.line',
        string='Previous Spread Line',
        readonly=True)
    amount = fields.Float(
        string='Amount',
        digits=dp.get_precision('Account'),
        required=True)
    remaining_value = fields.Float(
        string='Next Period Spread',
        digits=dp.get_precision('Account'))
    spreaded_value = fields.Float(
        string='Amount Already Spread',
        digits=dp.get_precision('Account'))
    line_date = fields.Date(
        string='Date',
        required=True)
    move_id = fields.Many2one(
        comodel_name='account.move',
        string='Spread Entry', readonly=True)

    type = fields.Selection(
        [('create', 'Value'),
         ('depreciate', 'Depreciation'),
         ('remove', 'Asset Removal'),
         ],
        string='Type',
        readonly=True,
        default='depreciate')

    @api.model
    def create(self, vals):
        context = self.env.context.copy()
        inv_types = ['in_invoice', 'in_refund', 'out_invoice', 'out_refund']
        if context.get('default_type', '') in inv_types:
            context.pop('default_type')
        res = super(
            AccountInvoiceSpreadLine,
            self.with_context(context)
        ).create(vals)
        return res

    @api.multi
    def _setup_move_data(self, spread_date):
        self.ensure_one()
        invoice = self.invoice_line_id.invoice_id
        journal = invoice.journal_id

        move_data = {
            'name': invoice and invoice.number or "/",
            'date': spread_date,
            'ref': self.name,
            'journal_id': journal.id,
            }
        return move_data

    @api.multi
    def _setup_move_line_data(self, spread_date,
                              account_id, type, move_id):
        self.ensure_one()
        invoice_line = self.invoice_line_id

        if type == 'debit':
            debit = self.amount
            credit = 0.0
        elif type == 'credit':
            debit = 0.0
            credit = self.amount

        move_line_data = {
            'name': invoice_line.name,
            'ref': self.name,
            'move_id': move_id,
            'account_id': account_id,
            'credit': credit,
            'debit': debit,
            'journal_id': invoice_line.invoice_id.journal_id.id,
            'partner_id': invoice_line.invoice_id.partner_id.id,
            'date': spread_date,
            'analytic_account_id': invoice_line.account_analytic_id.id,
            }
        if 'cost_center_id' in invoice_line._fields:
            move_line_data['cost_center_id'] = invoice_line.cost_center_id.id
        return move_line_data

    @api.multi
    def create_moves(self):
        for line in self:
            invoice_line = line.invoice_line_id
            if invoice_line and invoice_line.invoice_id:
                if invoice_line.invoice_id.number:
                    line.create_move()

    @api.multi
    def create_move(self):
        """
        Used by a button to manually create a move from a spread line entry.
        Also called by a cron job.
        """
        self.ensure_one()
        Move = self.env['account.move']

        invoice_line = self.invoice_line_id
        spread_date = self.line_date
        move_vals = self._setup_move_data(spread_date)
        move = Move.create(move_vals)
        _logger.debug('MoveID: %s', (move.id))

        if invoice_line.invoice_id.type in ('in_invoice', 'out_refund'):
            debit_acc_id = invoice_line.account_id.id
            credit_acc_id = invoice_line.spread_account_id.id
        else:
            debit_acc_id = invoice_line.spread_account_id.id
            credit_acc_id = invoice_line.account_id.id

        line_list = []
        line_list += [(0, 0, self._setup_move_line_data(
            spread_date, debit_acc_id,
            'debit', move.id
        ))]

        line_list += [(0, 0, self._setup_move_line_data(
            spread_date, credit_acc_id,
            'credit', move.id
        ))]

        move.write({'line_ids': line_list, })

        # Add move_id to spread line
        self.write({'move_id': move.id})

    @api.multi
    def open_move(self):
        """Used by a button to manually view a move from a
        spread line entry."""
        self.ensure_one()
        return {
            'name': _("Journal Entry"),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'domain': [('id', '=', self.move_id.id)],
            }

    @api.multi
    def unlink_move(self):
        """Used by a button to manually unlink a move
        from a spread line entry."""
        for line in self:
            move = line.move_id
            if move.state == 'posted':
                move.button_cancel()
            move.unlink()
            line.move_id = False

    @api.model
    def _create_entries(self, automatic=False):
        """Find spread line entries where date is in the past and
        create moves for them."""
        lines = self.search([
            ('line_date', '<=', fields.Date.today()),
            ('move_id', '=', False)]
        )
        lines.create_moves()
