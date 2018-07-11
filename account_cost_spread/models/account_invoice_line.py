# -*- coding: utf-8 -*-
# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import calendar
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
from odoo.tools import float_is_zero


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def _compute_spread_start_date(self):
        for line in self:
            date = line.spread_date
            if not date:
                date = line.invoice_id.date_invoice
            if not date:
                today = fields.Date.today()
                year = fields.Date.from_string(today).strftime('%Y')
                date = year + '-01-01'
            line.spread_start_date = date

    spread_date = fields.Date(string='Alternative Start Date')
    spread_start_date = fields.Date(compute='_compute_spread_start_date')
    period_number = fields.Integer(
        string='Number of Periods',
        default=12,
        help="Number of Periods",
        required=True)
    period_type = fields.Selection([
        ('month', 'Month'),
        ('quarter', 'Quarter'),
        ('year', 'Year'),
    ], default='month', help="Period length for the entries", required=True)
    spread_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Spread Account')
    remaining_amount = fields.Float(
        string='Residual Amount',
        digits=dp.get_precision('Account'),
        compute='_compute_remaining_amount')
    unposted_amount = fields.Float(
        string='Spread Amount',
        digits=dp.get_precision('Account'),
        compute='_compute_remaining_amount')
    spread_line_ids = fields.One2many(
        comodel_name='account.invoice.spread.line',
        inverse_name='invoice_line_id',
        string='Spread Lines')

    @api.multi
    @api.depends(
        'price_subtotal',
        'spread_line_ids.move_check',
        'spread_line_ids.move_posted_check',
        'spread_line_ids.amount')
    def _compute_remaining_amount(self):
        for line in self:
            total_amount = 0.0
            posted_amount = 0.0
            for spread_line in line.spread_line_ids:
                if spread_line.move_check:
                    total_amount += spread_line.amount
                if spread_line.move_posted_check:
                    posted_amount += spread_line.amount
            line.remaining_amount = line.price_subtotal - total_amount
            line.unposted_amount = line.price_subtotal - posted_amount

    @api.multi
    def spread_details(self):
        """Button on the invoice lines tree view on the invoice
        form to show the spread form view."""
        self.ensure_one()
        spread_view = self.env['ir.ui.view'].search(
            [('name', '=', 'account.invoice.line.spread')], limit=1)
        view_id = spread_view.id if spread_view else None

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
                last_spread_date = fields.Datetime.from_string(
                    posted_line_ids[-1].line_date
                ).date()
                spread_date = last_spread_date + relativedelta(months=+1)
            else:
                # spread_date computed from the purchase date
                spread_date = fields.Datetime.from_string(spread_start_date)
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
            lambda x: x.move_posted_check).sorted(key=lambda l: l.line_date)
        unposted_line_ids = self.spread_line_ids.filtered(
            lambda x: not x.move_posted_check)

        # Remove old unposted spread lines.
        # We cannot use unlink() with One2many field
        commands = [(2, line_id.id, False) for line_id in unposted_line_ids]

        if self.unposted_amount != 0.0:
            amount_to_spread = residual_amount = self.unposted_amount

            spread_date = _init_spread_date(
                self.spread_start_date, posted_line_ids)

            month_day = spread_date.day
            undone_dotation = self._compute_board_undone_dotation_nb(
                spread_date)

            for x in range(len(posted_line_ids), undone_dotation):
                sequence = x + 1
                amount = self._compute_board_amount(
                    sequence, residual_amount, amount_to_spread,
                    undone_dotation, posted_line_ids
                )
                amount = self.currency_id.round(amount)
                rounding = self.currency_id.rounding
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
                date = fields.Datetime.from_string(self.spread_start_date)
                month_days = calendar.monthrange(date.year, date.month)[1]
                days = month_days - date.day + 1
                period = self.period_number
                amount = (amount_to_spread / period) / month_days * days
        return amount

    @api.multi
    def is_all_set_for_spread(self):
        self.ensure_one()
        if not self.spread_account_id:
            return False
        return True

    @api.multi
    def compute_spread_board(self):
        for line in self:

            if not line.is_all_set_for_spread():
                continue

            if line.account_id.deprecated:
                raise UserError(
                    _("Account on one of the invoice lines you're trying"
                      "to validate is deprecated"))

            if line.spread_line_ids and line.price_subtotal < 0.0:
                raise UserError(
                    _("Cannot spread the negative amount of "
                      "one of the invoice lines")
                )

            if line.price_subtotal:
                line._compute_spread_board()

    @api.multi
    def action_recalculate_spread(self):
        """Recalculate spread"""
        self.mapped('spread_line_ids').filtered('move_id').unlink_move()
        return self.compute_spread_board()

    @api.multi
    def action_undo_spread(self):
        """Undo spreading: Remove all created moves, restore original account
        on move line"""
        for this in self:
            this.mapped('spread_line_ids').filtered('move_id').unlink_move()
            this.mapped('spread_line_ids').unlink()

            this.write({
                'spread_account_id': False,
            })
