# -*- coding: utf-8 -*-
# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare
import odoo.addons.decimal_precision as dp


class AccountInvoiceSpreadLine(models.Model):
    _name = 'account.invoice.spread.line'
    _description = 'Account Invoice Spread Lines'

    _order = 'line_date'

    name = fields.Char('Spread Name', readonly=True)
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
    move_check = fields.Boolean(
        compute='_compute_move_check',
        string='Linked',
        track_visibility='always',
        store=True)
    move_posted_check = fields.Boolean(
        compute='_compute_move_posted_check',
        string='Posted',
        track_visibility='always',
        store=True)
    sequence = fields.Integer(required=True, default=1)

    @api.multi
    @api.depends('move_id')
    def _compute_move_check(self):
        for line in self:
            line.move_check = bool(line.move_id)

    @api.multi
    @api.depends('move_id.state')
    def _compute_move_posted_check(self):
        for line in self:
            is_posted = line.move_id and line.move_id.state == 'posted'
            line.move_posted_check = True if is_posted else False

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

        created_moves = self.env['account.move']
        for line in self:
            if line.move_id:
                raise UserError(_('This spread line is already linked to a '
                                  'journal entry! Please post or delete it.'))
            move_vals = line._prepare_move()
            move = self.env['account.move'].create(move_vals)

            line.write({'move_id': move.id})
            created_moves |= move
        return [x.id for x in created_moves]

    @api.multi
    def _prepare_move(self):
        self.ensure_one()

        spread_date = self.env.context.get('spread_date') or self.line_date
        invoice_line = self.invoice_line_id
        invoice = invoice_line.invoice_id
        analytic = invoice_line.account_analytic_id

        if invoice.type in ('in_invoice', 'out_refund'):
            debit_acc_id = invoice_line.account_id.id
            credit_acc_id = invoice_line.spread_account_id.id
        else:
            debit_acc_id = invoice_line.spread_account_id.id
            credit_acc_id = invoice_line.account_id.id

        company_currency = invoice.company_id.currency_id
        current_currency = invoice_line.currency_id
        not_same_curr = company_currency != current_currency
        prec = company_currency.decimal_places
        date_amount = invoice.date or invoice.date_invoice or spread_date
        amount = current_currency.with_context(date=date_amount).compute(
            self.amount, company_currency)
        is_sale = invoice.journal_id.type == 'sale'
        is_purchase = invoice.journal_id.type == 'purchase'
        is_positive = float_compare(amount, 0.0, precision_digits=prec) > 0

        move_line_1 = {
            'name': invoice_line.name,
            'account_id': credit_acc_id if is_positive else debit_acc_id,
            'debit': 0.0 if is_positive else -amount,
            'credit': amount if is_positive else 0.0,
            'partner_id': invoice.partner_id.id,
            'analytic_account_id': analytic.id if is_sale else False,
            'currency_id': not_same_curr and current_currency.id or False,
            'amount_currency': not_same_curr and - 1.0 * self.amount or 0.0,
        }
        move_line_2 = {
            'name': invoice_line.name,
            'account_id': debit_acc_id if is_positive else credit_acc_id,
            'credit': 0.0 if is_positive else -amount,
            'debit': amount if is_positive else 0.0,
            'partner_id': invoice.partner_id.id,
            'analytic_account_id': analytic.id if is_purchase else False,
            'currency_id': not_same_curr and current_currency.id or False,
            'amount_currency': not_same_curr and self.amount or 0.0,
        }
        move_vals = {
            'name': invoice and invoice.number or "/",
            'ref': self.name,
            'date': spread_date or False,
            'journal_id': invoice.journal_id.id,
            'line_ids': [(0, 0, move_line_1), (0, 0, move_line_2)],
            'company_id': invoice.journal_id.company_id.id,
        }
        return move_vals

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
    def _create_entries(self):
        """Find spread line entries where date is in the past and
        create moves for them."""
        lines = self.search([
            ('line_date', '<=', fields.Date.today()),
            ('move_id', '=', False)
        ])
        lines.create_moves()
