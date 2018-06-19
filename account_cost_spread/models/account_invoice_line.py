# -*- coding: utf-8 -*-
# Copyright 2014 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import calendar
from dateutil.relativedelta import relativedelta

import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError, ValidationError
from openerp.tools import float_is_zero

PERIODS = [
    ('month', 'Month'),
    ('quarter', 'Quarter'),
    ('year', 'Year'),
]


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    spread_date = fields.Date(string='Alternative Start Date')
    spread_journal_id = fields.Many2one(
        'account.journal', string='Alternative journal',
    )
    period_number = fields.Integer(
        string='Number of Periods',
        default=12,
        help="Number of Periods",
        required=True)
    period_type = fields.Selection(
        PERIODS,
        default='month',
        help="Period length for the entries",
        required=True)
    spread_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Spread Account')
    remaining_amount = fields.Float(
        string='Residual Amount',
        digits=dp.get_precision('Account'),
        compute='_compute_remaining_amount')
    spreaded_amount = fields.Float(
        string='Spread Amount',
        digits=dp.get_precision('Account'),
        compute='_compute_remaining_amount')
    spread_line_ids = fields.One2many(
        comodel_name='account.invoice.spread.line',
        inverse_name='invoice_line_id',
        string='Spread Lines')
    spread_date_required = fields.Boolean(
        compute='_compute_spread_date_required')

    @api.multi
    def _compute_spread_date_required(self):
        for this in self:
            this.spread_date_required = not bool(this.invoice_id.date_invoice)

    @api.depends('spread_line_ids.amount', 'price_subtotal')
    def _compute_remaining_amount(self):
        for this in self:
            spread_amount = sum(this.mapped('spread_line_ids.amount'))
            this.update({
                'remaining_amount': this.price_subtotal - spread_amount,
                'spreaded_amount': spread_amount,
            })

    @api.constrains('spread_line_ids')
    def _check_spread_line_ids(self):
        for this in self:
            if not float_is_zero(
                    this.remaining_amount,
                    self.env['decimal.precision'].precision_get('Account'),
            ):
                raise ValidationError(_(
                    'You didn\'t distribute the total amount'
                ))

    @api.multi
    def spread_details(self):
        """Button on the invoice lines tree view on the invoice
        form to show the spread form view."""
        view_obj = self.env['ir.ui.view'].search([
            ('name', '=', 'account.invoice.line.spread'),
        ], limit=1)
        view_id = False
        if view_obj:
            view_id = view_obj.id

        view = {
            'name': _('Spread Details'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.line',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'readonly': False,
            'res_id': self.id,
            }
        return view

    @api.model
    def move_line_get_item(self, line):
        res = super(AccountInvoiceLine, self).move_line_get_item(line)
        if line.spread_account_id:
            res.update({'account_id': line.spread_account_id.id})
        return res

    @api.multi
    def _get_spread_entry_name(self, seq):
        """ use this method to customise the name of the accounting entry """
        self.ensure_one()
        return (self.name or str(self.id)) + '/' + str(seq)

    @api.multi
    def _compute_spread_board(self):
        self.ensure_one()

        def _init_spread_date(spread_start_date, posted_line_ids):
            # if we already have some previous validated entries,
            # starting date is last entry + method period
            if posted_line_ids and posted_line_ids[-1].line_date:
                last_spread_date = fields.Date.from_string(
                    posted_line_ids[-1].line_date
                ).date()
                spread_date = last_spread_date + relativedelta(months=+1)
            else:
                # spread_date computed from the purchase date
                spread_date = fields.Date.from_string(spread_start_date)
            return spread_date

        def _increase_spread_date(month_day, spread_date):
            spread_date = spread_date + relativedelta(months=+1)
            if month_day > 28:
                max_day_in_month = calendar.monthrange(
                    spread_date.year, spread_date.month
                )[1]
                spread_date = spread_date.replace(
                    day=min(max_day_in_month, month_day)
                )
            return spread_date

        posted_line_ids = self.spread_line_ids.filtered(
            lambda x: x.move_id.state == 'posted'
        ).sorted(key=lambda l: l.line_date)
        unposted_line_ids = self.spread_line_ids.filtered(
            lambda x: x.move_id.state != 'posted'
        )

        # Remove old unposted spread lines.
        unposted_line_ids.unlink()
        commands = []

        if self.remaining_amount != 0:
            amount_to_spread = residual_amount = self.remaining_amount

            spread_date = _init_spread_date(
                self.spread_date or self.invoice_id.date_invoice,
                posted_line_ids,
            )

            month_day = spread_date.day
            undone_dotation = self._compute_board_undone_dotation_nb(
                spread_date)

            for x in range(len(posted_line_ids), undone_dotation):
                sequence = x + 1
                amount = self._compute_board_amount(
                    sequence, residual_amount, amount_to_spread,
                    undone_dotation, posted_line_ids
                )
                amount = self.invoice_id.currency_id.round(amount)
                rounding = self.invoice_id.currency_id.rounding
                if float_is_zero(amount, precision_rounding=rounding):
                    continue
                residual_amount -= amount
                vals = {
                    'amount': amount,
                    'invoice_line_id': self.id,
                    'sequence': sequence,
                    'name': self._get_spread_entry_name(sequence),
                    'remaining_value': residual_amount,
                    'spreaded_value': self.price_subtotal - (residual_amount),
                    'line_date': self._get_line_date(spread_date),
                }
                commands.append((0, False, vals))

                spread_date = _increase_spread_date(month_day, spread_date)

        self.write({'spread_line_ids': commands})

        return True

    @staticmethod
    def _get_line_date(spread_date):
        date = spread_date + relativedelta(day=31)
        line_date = fields.Date.to_string(date)
        return line_date

    def _compute_board_undone_dotation_nb(self, spread_date):
        undone_dotation_number = self.period_number
        spread_day = spread_date.day
        if spread_day != 1:
            undone_dotation_number += 1
        return undone_dotation_number

    def _compute_board_amount(self, sequence, residual_amount,
                              amount_to_spread, undone_dotation_number,
                              posted_spread_line_ids):
        amount = residual_amount
        if sequence != undone_dotation_number:
            amount = amount_to_spread / (
                self.period_number - len(posted_spread_line_ids)
            )
            if sequence == 1:
                date = fields.Date.from_string(
                    self.spread_date or self.invoice_id.date_invoice,
                )
                month_days = calendar.monthrange(date.year, date.month)[1]
                days = month_days - date.day + 1
                period = self.period_number
                amount = (amount_to_spread / period) / month_days * days
        return amount

    @api.multi
    def compute_spread_board(self):
        for line in self:

            if line.spread_line_ids and line.price_subtotal < 0.0:
                raise UserError(
                    _("Cannot spread the negative amount of "
                      "one of the invoice lines")
                )

            if line.price_subtotal:
                line._compute_spread_board()

    @api.multi
    def _find_move_line(self):
        """Look up the move lines mapped to this invoice lines"""
        result = self.env['account.move.line'].browse([])
        for this in self:
            move_line_data = this.move_line_get_item(this)
            # correct name difference between move and lin
            if 'account_analytic_id' in move_line_data.keys():
                move_line_data['analytic_account_id'] = move_line_data.pop(
                    'account_analytic_id'
                )

            sign = -1 if this.invoice_id.type in [
                'in_refund', 'out_invoice'
            ] else 1
            price = move_line_data['price'] * sign
            move_line_data.update(
                debit=price > 0 and price,
                credit=price < 0 and -price,
            )

            # clean non existing fields
            for key in move_line_data.keys():
                if key not in result._fields:
                    move_line_data.pop(key)
            result += this.invoice_id.move_id.line_id.filtered(
                lambda x, mld=move_line_data: mld == {
                    key: value
                    for key, value in x.read(
                        mld.keys(), load='_classic_write',
                    )[0].iteritems() if key != 'id'
                }
            )
        return result

    @api.multi
    def unlink_reconciliations(self):
        self.mapped('spread_line_ids.move_id.line_id.reconcile_id').unlink()
        self.mapped(
            'spread_line_ids.move_id.line_id.reconcile_partial_id'
        ).unlink()

    @api.multi
    def action_undo_spread(self):
        """Undo spreading: Remove all created moves, restore original account
        on move line"""
        for this in self:
            spread_lines = this.mapped('spread_line_ids')
            moves = spread_lines.filtered('move_id')
            # deleting reconciliation work is being put into
            # unlink_reconciliation
            if this.spread_account_id.reconcile:
                this.unlink_reconciliations()
            moves.unlink_move()
            spread_lines.unlink()
            move_line = this._find_move_line()
            if not move_line and\
                    this.invoice_id.journal_id.group_invoice_lines:
                raise UserError(_(
                    'Cannot reliably determine accounting entry on grouped '
                    'journal'
                ))
            posted = move_line.move_id.state == 'posted'
            if posted:
                move_line.move_id.button_cancel()
            move_line.write({
                'account_id': this.account_id.id,
            })
            if posted:
                move_line.move_id.button_validate()
            this.write({
                'spread_account_id': False,
            })

    @api.multi
    def action_recalculate_spread(self):
        """Recalculate spread"""
        self.mapped('spread_line_ids').filtered('move_id').unlink_move()
        return self.compute_spread_board()
