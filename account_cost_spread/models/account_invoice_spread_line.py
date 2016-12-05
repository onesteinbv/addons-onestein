# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import calendar
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
import logging

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
        defaults='depreciate')

    @api.model
    def create(self, values):
        context = self.env.context.copy()
        if context.get('default_type', '') == 'in_invoice':
            context.pop('default_type')
        return super(
            AccountInvoiceSpreadLine,
            self.with_context(context)
        ).create(values)

    @api.model
    def _setup_move_data(self, spread_line, spread_date):

        invoice = spread_line.invoice_line_id.invoice_id

        move_data = {
            'name': invoice.number,
            'date': spread_date,
            'ref': spread_line.name,
            'journal_id': invoice.journal_id.id,
            }
        return move_data

    @api.model
    def _setup_move_line_data(self, spread_line, spread_date,
                              account_id, type, move_id):
        invoice_line = spread_line.invoice_line_id

        if type == 'debit':
            debit = spread_line.amount
            credit = 0.0
        elif type == 'credit':
            debit = 0.0
            credit = spread_line.amount

        move_line_data = {
            'name': invoice_line.name,
            'ref': spread_line.name,
            'move_id': move_id,
            'account_id': account_id,
            'credit': credit,
            'debit': debit,
            'journal_id': invoice_line.invoice_id.journal_id.id,
            'partner_id': invoice_line.invoice_id.partner_id.id,
            'date': spread_date,
            }
        return move_line_data

    @api.multi
    def create_move(self):
        """
        Used by a button to manually create a move from a spread line entry.
        Also called by a cron job.
        """

        move_obj = self.env['account.move']
#         currency_obj = self.env['res.currency']
        created_move_ids = []

        for line in self:

            invoice_line = line.invoice_line_id
            spread_date = line.line_date

            move_id = move_obj.create(
                self._setup_move_data(line, spread_date)
            )
            _logger.debug('MoveID: %s', (move_id.id))

            if invoice_line.invoice_id.type in ('in_invoice', 'out_refund'):
                debit_acc_id = invoice_line.account_id.id
                credit_acc_id = invoice_line.spread_account_id.id
            else:
                debit_acc_id = invoice_line.spread_account_id.id
                credit_acc_id = invoice_line.account_id.id

            line_list = []
            line_list += [(0, 0, self._setup_move_line_data(
                line, spread_date, debit_acc_id,
                'debit', move_id.id
            ))]

            line_list += [(0, 0, self._setup_move_line_data(
                line, spread_date, credit_acc_id,
                'credit', move_id.id
            ))]

            move_id.write({'line_ids': line_list, })

            # Add move_id to spread line
            line.write({'move_id': move_id.id})

            created_move_ids.append(move_id.id)

        return created_move_ids

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
        return True

    @api.model
    def _create_entries(self, automatic=False):
        """Find spread line entries where date is in the past and
        create moves for them."""
        today = fields.Date.from_string(fields.Date.today())
        year = today.strftime('%Y')
        month = today.strftime('%m')
        month_range = calendar.monthrange(int(year), int(month.lstrip('0')))
        end_date = today.replace(day=month_range[1])

        lines = self.search([('line_date', '<=', end_date),
                             ('move_id', '=', False)])

        result = []
        for line in lines:
            result += line.create_move()

        return result
