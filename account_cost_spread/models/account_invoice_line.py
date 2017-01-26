# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import calendar
from datetime import datetime
from functools import reduce

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
import odoo.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    spread_date = fields.Date(string='Alternative Start Date')
    period_number = fields.Integer(
        string='Number of Periods',
        default=12,
        help="Number of Periods",
        required=True)
    period_type = fields.Selection([
        ('month', 'Month'),
        ('quarter', 'Quarter'),
        ('year', 'Year'),
        ],
        default='month',
        help="Period length for the entries",
        required=True)
    spread_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Spread Account')
    remaining_amount = fields.Float(
        string='Residual Amount',
        digits=dp.get_precision('Account'))
    spreaded_amount = fields.Float(
        string='Spread Amount',
        digits=dp.get_precision('Account'))
    spread_line_ids = fields.One2many(
        comodel_name='account.invoice.spread.line',
        inverse_name='invoice_line_id',
        string='Spread Lines')

    @api.multi
    def spread_details(self):
        """Button on the invoice lines tree view on the invoice
        form to show the spread form view."""
        self.ensure_one()
        spread_view = self.env['ir.ui.view'].search(
            [('name', '=', 'account.invoice.line.spread')], limit=1)
        view_id = spread_view and spread_view.id or None

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
    def _get_fy_duration(self, fy_dates):

        def get_factor(cnt, cy_days, factor, i, year):
            fy_date_start = datetime.strptime(
                fy_dates['date_from'].strftime('%Y-%m-%d'), '%Y-%m-%d'
            )
            fy_date_stop = datetime.strptime(
                fy_dates['date_to'].strftime('%Y-%m-%d'), '%Y-%m-%d'
            )
            if i == 0:  # first year
                duration = (datetime(year, 12, 31) - fy_date_start).days + 1
                if fy_date_stop.year == year:
                    duration = (fy_date_stop - fy_date_start).days + 1

                factor = float(duration) / cy_days
            elif i == cnt - 1:  # last year
                duration = fy_date_stop - datetime(year, 1, 1)
                duration_days = duration.days + 1
                factor += float(duration_days) / cy_days
            else:
                factor += 1.0
            return factor

        fy_year_start = int(fy_dates['date_from'].strftime('%Y-%m-%d')[:4])
        fy_year_stop = int(fy_dates['date_to'].strftime('%Y-%m-%d')[:4])
        year = fy_year_start
        cnt = fy_year_stop - fy_year_start + 1
        factor = 0
        for i in range(cnt):
            cy_days = calendar.isleap(year) and 366 or 365
            factor = get_factor(cnt, cy_days, factor, i, year)
            year += 1
        return factor

    @api.multi
    def _get_fy_dates(self):
        self.ensure_one()
        date_invoice = self.invoice_id.date_invoice
        date_invoice_formatted = datetime.strptime(date_invoice, DF)
        fy_dates = self.company_id.compute_fiscalyear_dates(
            date_invoice_formatted.date()
        )
        return fy_dates

    @api.multi
    def _get_fy_duration_factor(self, entry, firstyear):
        self.ensure_one()
        date_invoice = self.invoice_id.date_invoice or fields.Date.today()
        if firstyear:
            spread_date_start = datetime.strptime(
                date_invoice, '%Y-%m-%d')
            if self.spread_date:
                spread_date_start = datetime.strptime(
                    self.spread_date, '%Y-%m-%d')
            fy_date_stop = entry['date_stop']
            first_fy_spread_days = \
                (fy_date_stop - spread_date_start.date()).days + 1

            first_fy_duration = \
                calendar.isleap(entry['date_start'].year) \
                and 366 or 365
            duration_factor = \
                float(first_fy_spread_days) / first_fy_duration
        else:
            fy_dates = self._get_fy_dates()
            duration_factor = self._get_fy_duration(fy_dates)

        return duration_factor

    @api.multi
    def _get_spread_start_date(self):
        self.ensure_one()
        fy_dates = self._get_fy_dates()

        date_start = fy_dates['date_from']
        if self.spread_date:
            spread_start_date = datetime.strptime(
                self.spread_date, '%Y-%m-%d')
        elif self.invoice_id.date_invoice:
            spread_start_date = datetime.strptime(
                self.invoice_id.date_invoice, '%Y-%m-%d')
        else:
            fy_date_start = datetime.strptime(date_start, '%Y-%m-%d')
            spread_start_date = datetime(
                fy_date_start.year, fy_date_start.month, 1
            )
        return spread_start_date

    @api.multi
    def _get_spread_stop_date(self):
        self.ensure_one()
        spread_start_date = self._get_spread_start_date()
        spread_stop_date = None
        if self.period_type == 'month':
            spread_stop_date = spread_start_date + relativedelta(
                months=self.period_number, days=-1)
        elif self.period_type == 'quarter':
            spread_stop_date = spread_start_date + relativedelta(
                months=self.period_number * 3, days=-1)
        elif self.period_type == 'year':
            spread_stop_date = spread_start_date + relativedelta(
                years=self.period_number, days=-1)
        return spread_stop_date

    @api.multi
    def _compute_year_amount(self):
        self.ensure_one()
        factor = 1
        if self.period_type == 'month':
            factor = self.period_number / 12.0
        elif self.period_type == 'quarter':
            factor = self.period_number * 3 / 12.0
        elif self.period_type == 'year':
            factor = self.period_number

        period_amount = self.price_subtotal / factor
        return period_amount

    @api.multi
    def _compute_spread_table(self):
        self.ensure_one()
        table = []
        if not self.period_number or \
                not self.spread_account_id or \
                not self.period_type:
            return table

        self._init_spread_table(table)
        i_max, table = self._compute_spread_table_entries(table)
        self._compute_spread_table_lines(i_max, table)

        return table

    @api.multi
    def _compute_spread_table_entries(self, table):
        # step 1:
        # teble headers
        # calculate spread amount per fiscal year
        self.ensure_one()
        digits = self.env['decimal.precision'].precision_get('Account')
        fy_residual_amount = self.price_subtotal
        i_max = len(table) - 1
        invoice_sign = self.price_subtotal >= 0 and 1 or -1
        for i, entry in enumerate(table):
            if i == i_max:
                fy_amount = fy_residual_amount
            else:
                firstyear = i == 0 and True or False
                fy_factor = self._get_fy_duration_factor(entry, firstyear)
                year_amount = self._compute_year_amount()
                fy_amount = year_amount * fy_factor
            if invoice_sign * (fy_amount - fy_residual_amount) > 0:
                fy_amount = fy_residual_amount
            fy_amount = round(fy_amount, digits)
            entry.update({
                'period_amount': self._compute_period_amount(),
                'fy_amount': fy_amount,
            })
            fy_residual_amount -= fy_amount
            if round(fy_residual_amount, digits) == 0:
                break
        i_max = i
        table = table[:i_max + 1]
        return i_max, table

    @api.multi
    def _compute_spread_table_lines(self, i_max, table):
        # step 2: spread amount per fiscal year
        # over the periods
        self.ensure_one()
        amount_to_spread = self.price_subtotal
        residual_amount = self.price_subtotal
        for i, entry in enumerate(table):
            lines = self._compute_lines(entry, i, i_max, residual_amount)
            for line in lines:
                line['spreaded_value'] = amount_to_spread - residual_amount
                residual_amount -= line['amount']
                line['remaining_value'] = residual_amount
            entry['lines'] = lines

    @api.multi
    def _compute_lines(self, entry, i, i_max, residual_amount):
        self.ensure_one()

        def compute_lines_year(entry, sign, period_duration, residual_amount):
            fy_amount = entry['fy_amount']
            if sign * (fy_amount - residual_amount) > 0:
                fy_amount = residual_amount
            lines = [{'date': entry['date_stop'], 'amount': fy_amount}]
            residual_amount -= fy_amount
            return fy_amount, lines, residual_amount

        def compute_lines_month(
                entry, i, i_max, invoice_sign, line_date, period_amount,
                period_duration, residual_amount, spread_stop_date):
            lines = []
            fy_amount_check = 0.0
            entry_date_stop = entry['date_stop']
            min_stop = min(entry_date_stop, spread_stop_date.date())
            left = invoice_sign * (residual_amount - period_amount) > 0
            while line_date <= min_stop and left:
                lines.append({'date': line_date, 'amount': period_amount})
                residual_amount -= period_amount
                fy_amount_check += period_amount
                delta = relativedelta(months=period_duration, day=31)
                line_date = line_date + delta
                left = invoice_sign * (residual_amount - period_amount) > 0
            last_date = lines and lines[-1]['date'] or line_date
            is_end = spread_stop_date.date() > last_date
            if i == i_max and (not lines or is_end):
                # last year, last entry
                period_amount = residual_amount
                lines.append({'date': line_date, 'amount': period_amount})
                fy_amount_check += period_amount
            return fy_amount_check, lines, period_amount

        def round_lines(fy_amount_diff, i, lines, period_amount):
            digits = self.env['decimal.precision'].precision_get('Account')
            if round(fy_amount_diff, digits) != 0:
                # handle rounding and extended/shortened
                # fiscal year deviations
                if i == 0:  # first year: deviation in first period
                    lines[0]['amount'] = period_amount - fy_amount_diff
                else:  # other years: deviation in last period
                    lines[-1]['amount'] = period_amount - fy_amount_diff

        spread_stop_date = self._get_spread_stop_date()
        invoice_sign = self.price_subtotal >= 0 and 1 or -1
        line_date = False
        period_amount = entry['period_amount']
        fy_amount = entry['fy_amount']
        period_duration = self._get_period_duration()
        if period_duration == 12:
            fy_amount, lines, residual_amount = compute_lines_year(
                entry, invoice_sign, period_duration, residual_amount)
        else:
            line_date = self._update_line_date(line_date)
            fy_amount_check, lines, period_amount = self.compute_lines_month(
                entry, i, i_max, invoice_sign, line_date,
                period_amount, period_duration,
                residual_amount, spread_stop_date
            )
            fy_amount_diff = fy_amount_check - fy_amount
            round_lines(fy_amount_diff, i, lines, period_amount)
        return lines

    @api.multi
    def _update_line_date(self, line_date):
        period_duration = self._get_period_duration()
        spread_start_date = self._get_spread_start_date()
        if not line_date:
            delta = relativedelta(months=0, day=31)
            line_date = spread_start_date.date() + delta
            if period_duration == 3:
                first_month = None
                for x in [3, 6, 9, 12]:
                    if x >= spread_start_date.month:
                        first_month = x
                        break
                delta = relativedelta(month=first_month, day=31)
                line_date = spread_start_date.date() + delta
        return line_date

    @api.multi
    def _get_period_duration(self):
        period_duration = (self.period_type == 'year' and 12) or \
                          (self.period_type == 'quarter' and 3) or 1
        if period_duration not in [1, 3, 12]:
            raise Warning(
                _('Programming Error!'),
                _("Illegal value %s in invline.period_type.")
                % self.period_type)
        return period_duration

    @api.multi
    def _init_spread_table(self, table):
        self.ensure_one()

        fy_dates = self._get_fy_dates()

        init_flag = True
        fy_date_start = fy_dates['date_from']
        fy_date_stop = fy_dates['date_to']
        spread_stop_date = self._get_spread_stop_date()
        while fy_date_start <= spread_stop_date.date():
            table.append({
                'date_start': fy_date_start,
                'date_stop': fy_date_stop,
                'init': init_flag})
            fy_date_start = fy_date_stop + relativedelta(days=1)
            fy_date_stop = fy_date_stop + relativedelta(years=1)

    @api.multi
    def _compute_period_amount(self):
        self.ensure_one()
        digits = self.env['decimal.precision'].precision_get('Account')
        year_amount = self._compute_year_amount()
        period_amount = year_amount
        if self.period_type == 'year':
            period_amount = year_amount
        elif self.period_type == 'quarter':
            period_amount = year_amount / 4
        elif self.period_type == 'month':
            period_amount = year_amount / 12
        period_amount = round(period_amount, digits)
        return period_amount

    @api.multi
    def _get_spread_entry_name(self, seq):
        """ use this method to customise the name of the accounting entry """
        self.ensure_one()
        return (self.name or str(self.id)) + '/' + str(seq)

    @api.multi
    def compute_spread_board(self):
        for invline in self:
            if invline.price_subtotal == 0.0:
                continue
            invline._unlink_old_spreads()
            table = invline._compute_spread_table()
            if not table:
                continue
            invline._compute_spread_board(table)

    @api.multi
    def _compute_spread_board(self, table):
        self.ensure_one()

        def spread_line_vals(amount, line, name, invoice_line_id):
            return {
                'amount': amount,
                'invoice_line_id': invoice_line_id,
                'name': name,
                'line_date': line['date'].strftime('%Y-%m-%d'),
            }

        SpreadLine = self.env['account.invoice.spread.line']

        self._group_table_lines(table)
        line_i_start = table_i_start = 0

        seq = 0
        last_date = table[-1]['lines'][-1]['date']
        for entry in table[table_i_start:]:
            for line in entry['lines'][line_i_start:]:
                seq += 1
                name = self._get_spread_entry_name(seq)
                amount = self._get_amount(last_date, line)
                vals = spread_line_vals(amount, line, name, self.id)
                SpreadLine.create(vals)
            line_i_start = 0

    @api.multi
    def _group_table_lines(self, table):
        # group lines prior to spread start period
        self.ensure_one()
        spread_start = self.spread_date or self.invoice_id.date_invoice
        spread_start_date = datetime.strptime(spread_start, '%Y-%m-%d')
        lines = table[0]['lines']
        lines1 = []
        lines2 = []
        line_date = lines[0]['date']
        flag = line_date < spread_start_date.date()
        for line in lines:
            if flag:
                lines1.append(line)
                if line['date'] >= spread_start_date:
                    flag = False
            else:
                lines2.append(line)
        if lines1:
            def group_lines(x, y):
                y.update({'amount': x['amount'] + y['amount']})
                return y

            lines1 = [reduce(group_lines, lines1)]
            lines1[0]['spreaded_value'] = 0.0
        table[0]['lines'] = lines1 + lines2

    @api.multi
    def _get_amount(self, last_date, line):
        self.ensure_one()

        def get_last_amount(last_date, spreads):
            # ensure that the last entry of the table always
            # depreciates the remaining value
            filtered_spreads = []
            for spread in spreads:
                line_date = datetime.strptime(spread.line_date, DF).date()
                if line_date < last_date:
                    filtered_spreads.append(spread)

            existing_amount = 0.0
            for existspread in filtered_spreads:
                existing_amount += existspread.amount
            return existing_amount

        amount = line['amount']
        if line['date'] == last_date:
            spreads = self.spread_line_ids
            existing_amount = get_last_amount(last_date, spreads)
            amount = self.price_subtotal - existing_amount
        return amount

    @api.multi
    def _unlink_old_spreads(self):
        for line in self:
            to_remove = line.spread_line_ids.filtered(
                lambda l: l.type == 'depreciate' and not l.move_id
            )
            to_remove.unlink()
