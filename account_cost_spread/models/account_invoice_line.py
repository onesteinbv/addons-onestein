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

    @api.multi
    def _compute_spread_stop_date(self):
        for line in self:
            start_date = line.spread_start_date
            spread_start_date = datetime.strptime(start_date, '%Y-%m-%d')

            spread_stop_date = None
            if line.period_type == 'month':
                spread_stop_date = spread_start_date + relativedelta(
                    months=line.period_number, days=-1)
            elif line.period_type == 'quarter':
                spread_stop_date = spread_start_date + relativedelta(
                    months=line.period_number * 3, days=-1)
            elif line.period_type == 'year':
                spread_stop_date = spread_start_date + relativedelta(
                    years=line.period_number, days=-1)
            spread_stop_date = spread_stop_date.strftime('%Y-%m-%d')
            line.spread_stop_date = spread_stop_date

    @api.multi
    def _compute_year_amount(self):
        for line in self:
            factor = 1
            if line.period_type == 'month':
                factor = line.period_number / 12.0
            elif line.period_type == 'quarter':
                factor = line.period_number * 3 / 12.0
            elif line.period_type == 'year':
                factor = line.period_number

            line.year_amount = line.price_subtotal / factor

    @api.multi
    def _compute_period_amount(self):
        for line in self:
            period_amount = line.year_amount
            if self.period_type == 'quarter':
                period_amount = line.year_amount / 4
            elif self.period_type == 'month':
                period_amount = line.year_amount / 12
            line.period_amount = period_amount

    spread_date = fields.Date(string='Alternative Start Date')
    spread_start_date = fields.Date(compute='_compute_spread_start_date')
    spread_stop_date = fields.Date(compute='_compute_spread_stop_date')
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
    year_amount = fields.Float(
        compute='_compute_year_amount',
        string='Year Amount',
        digits=dp.get_precision('Account'))
    period_amount = fields.Float(
        compute='_compute_period_amount',
        string='Period Amount',
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

    @api.multi
    def _get_fy_duration(self, invoice_date, option='days'):
        """
        Returns fiscal year duration.
        @param option:
        - days: duration in days
        - months: duration in months,
                  a started month is counted as a full month
        - years: duration in calendar years, considering also leap years
        """

        def get_years(fy_dates):
            fy_date_start = datetime.strptime(
                fy_dates['date_from'].strftime('%Y-%m-%d'), '%Y-%m-%d')
            fy_year_start = int(fy_dates['date_from'].strftime('%Y-%m-%d')[:4])
            fy_date_stop = datetime.strptime(
                fy_dates['date_to'].strftime('%Y-%m-%d'), '%Y-%m-%d')
            fy_year_stop = int(fy_dates['date_to'].strftime('%Y-%m-%d')[:4])
            year = fy_year_start
            cnt = fy_year_stop - fy_year_start + 1
            factor = 0
            for i in range(cnt):
                cy_days = calendar.isleap(year) and 366 or 365
                if i == 0:  # first year
                    if fy_date_stop.year == year:
                        duration = (fy_date_stop - fy_date_start).days + 1
                    else:
                        duration = (datetime(year, 12, 31) -
                                    fy_date_start).days + 1
                    factor = float(duration) / cy_days
                elif i == cnt - 1:  # last year
                    duration = fy_date_stop - datetime(year, 1, 1)
                    duration_days = duration.days + 1
                    factor += float(duration_days) / cy_days
                else:
                    factor += 1.0
                year += 1
            return factor

        def get_months(fy_dates):
            months = (int(fy_dates['date_to'].strftime('%Y-%m-%d')[:4]) -
                      int(fy_dates['date_from'].strftime('%Y-%m-%d')[:4])
                      ) * 12 + \
                     (int(fy_dates['date_to'].strftime('%Y-%m-%d')[5:7]) -
                      int(fy_dates['date_from'].strftime('%Y-%m-%d')[5:7])
                      ) + 1
            return months

        def get_days(date_invoice_formatted, fy_dates):
            days = (fy_dates['date_to'] - date_invoice_formatted).days + 1
            return days

        self.ensure_one()
        date_invoice_formatted = datetime.strptime(invoice_date, DF).date()
        fy_dates = self.company_id.compute_fiscalyear_dates(
            date_invoice_formatted
        )

        if option == 'days':
            days = get_days(date_invoice_formatted, fy_dates)
            return days
        elif option == 'months':
            months = get_months(fy_dates)
            return months
        elif option == 'years':
            factor = get_years(fy_dates)
            return factor

    @api.multi
    def _get_fy_duration_factor(self, entry, firstyear):

        def factor_firstyear(date_invoice, entry, date):
            spread_date_start = datetime.strptime(date_invoice, '%Y-%m-%d')
            if date:
                spread_date_start = datetime.strptime(date, '%Y-%m-%d')
            fy_date_stop = entry['date_stop']
            first_fy_spread_days = \
                (fy_date_stop - spread_date_start.date()).days + 1
            first_fy_duration = \
                calendar.isleap(entry['date_start'].year) and 366 or 365
            fy_factor = float(first_fy_spread_days) / first_fy_duration
            return fy_factor

        self.ensure_one()
        date_invoice = self.invoice_id.date_invoice or fields.Date.today()
        fy_factor = factor_firstyear(date_invoice, entry, self.spread_date)
        if not firstyear:
            fy_factor = self._get_fy_duration(date_invoice, option='years')

        return fy_factor

    @api.multi
    def _compute_spread_table(self):
        self.ensure_one()

        def check_all_set(self):
            all_set = self.period_number and \
                      self.spread_account_id and \
                      self.period_type
            return all_set

        def get_format_date(date):
            return datetime.strptime(date, '%Y-%m-%d')

        def init_table(fy_dates, spread_stop_date, table):
            init_flag = True
            fy_date_start = fy_dates['date_from']
            fy_date_stop = fy_dates['date_to']
            while fy_date_start <= spread_stop_date.date():
                table.append({
                    'date_start': fy_date_start,
                    'date_stop': fy_date_stop,
                    'init': init_flag})
                fy_date_start = fy_date_stop + relativedelta(days=1)
                fy_date_stop = fy_date_stop + relativedelta(years=1)

        table = []
        if not check_all_set(self):
            return table

        date_invoice = self.invoice_id.date_invoice
        date_invoice_formatted = datetime.strptime(date_invoice, DF).date()
        fy_dates = self.company_id.compute_fiscalyear_dates(
            date_invoice_formatted)

        spread_start_date = get_format_date(self.spread_start_date)
        spread_stop_date = get_format_date(self.spread_stop_date)

        init_table(fy_dates, spread_stop_date, table)

        digits = self.env['decimal.precision'].precision_get('Account')
        amount_to_spread = residual_amount = self.price_subtotal

        # step 1:
        # calculate spread amount per fiscal year
        i_max, invoice_sign, table = self._compute_spread_table_entries(
            residual_amount, table)

        # step 2: spread amount per fiscal year
        # over the periods
        self._compute_spread_table_lines(
            self.period_type, amount_to_spread, i_max, invoice_sign,
            residual_amount, spread_start_date, spread_stop_date, table)

        return table

    @api.multi
    def _compute_spread_table_entries(self, residual_amount, table):
        self.ensure_one()
        digits = self.env['decimal.precision'].precision_get('Account')
        fy_residual_amount = residual_amount
        i_max = len(table) - 1
        invoice_sign = self.price_subtotal >= 0 and 1 or -1
        for i, entry in enumerate(table):
            year_amount = self.year_amount
            period_amount = self.period_amount
            if i == i_max:
                fy_amount = fy_residual_amount
            else:
                firstyear = i == 0 and True or False
                fy_factor = self._get_fy_duration_factor(entry, firstyear)
                fy_amount = year_amount * fy_factor
            if invoice_sign * (fy_amount - fy_residual_amount) > 0:
                fy_amount = fy_residual_amount
            period_amount = round(period_amount, digits)
            fy_amount = round(fy_amount, digits)
            entry.update({
                'period_amount': period_amount,
                'fy_amount': fy_amount,
            })
            fy_residual_amount -= fy_amount
            if round(fy_residual_amount, digits) == 0:
                break
        i_max = i
        table = table[:i_max + 1]
        return i_max, invoice_sign, table

    @api.model
    def _compute_spread_table_lines(
            self, period_type, amount_to_spread, i_max, invoice_sign,
            residual_amount, spread_start_date, spread_stop_date, table):
        digits = self.env['decimal.precision'].precision_get('Account')
        fy_residual_amount = residual_amount
        line_date = False
        for i, entry in enumerate(table):
            period_amount = entry['period_amount']
            fy_amount = entry['fy_amount']
            period_duration = (period_type == 'year' and 12) \
                              or (period_type == 'quarter' and 3) or 1
            if period_duration == 12:
                if invoice_sign * (fy_amount - fy_residual_amount) > 0:
                    fy_amount = fy_residual_amount
                lines = [{'date': entry['date_stop'], 'amount': fy_amount}]
                fy_residual_amount -= fy_amount
            elif period_duration in [1, 3]:
                lines = []
                fy_amount_check = 0.0
                if not line_date:
                    if period_duration == 3:
                        m = [x for x in [3, 6, 9, 12]
                             if x >= spread_start_date.month][0]
                        line_date = spread_start_date + \
                                    relativedelta(month=m, day=31)
                    else:
                        line_date = spread_start_date + \
                                    relativedelta(months=0, day=31)
                date_spread_stop_date = spread_stop_date.date()
                entry_date_stop = entry['date_stop']
                while line_date.date() <= \
                        min(entry_date_stop, date_spread_stop_date) and \
                                        invoice_sign * (
                                            fy_residual_amount - period_amount) > 0:
                    lines.append({'date': line_date, 'amount': period_amount})
                    fy_residual_amount -= period_amount
                    fy_amount_check += period_amount
                    line_date = line_date + \
                                relativedelta(months=period_duration, day=31)
                if i == i_max and \
                        (not lines or
                                 spread_stop_date > lines[-1]['date']):
                    # last year, last entry
                    period_amount = fy_residual_amount
                    lines.append({'date': line_date, 'amount': period_amount})
                    fy_amount_check += period_amount
                if round(fy_amount_check - fy_amount, digits) != 0:
                    # handle rounding and extended/shortened
                    # fiscal year deviations
                    diff = fy_amount_check - fy_amount
                    fy_residual_amount += diff
                    if i == 0:  # first year: deviation in first period
                        lines[0]['amount'] = period_amount - diff
                    else:  # other years: deviation in last period
                        lines[-1]['amount'] = period_amount - diff
            else:
                raise Warning(
                    _('Programming Error!'),
                    _("Illegal value %s in invline.period_type.")
                    % period_type)
            for line in lines:
                line['spreaded_value'] = amount_to_spread - residual_amount
                residual_amount -= line['amount']
                line['remaining_value'] = residual_amount
            entry['lines'] = lines

    @api.multi
    def _get_spread_entry_name(self, seq):
        """ use this method to customise the name of the accounting entry """
        self.ensure_one()
        return (self.name or str(self.id)) + '/' + str(seq)

    @api.multi
    def _compute_spread_board(self):
        self.ensure_one()

        def get_format_date(date):
            return datetime.strptime(date, '%Y-%m-%d')

        def get_last_spread_line(posted_spreads):
            last_spread_line = False
            if posted_spreads:
                last_spread_line = posted_spreads[0]
            return last_spread_line

        def compute_lines(spread_start_date, table):
            lines = table[0]['lines']
            lines1 = []
            lines2 = []
            flag = lines[0]['date'] < spread_start_date
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
            return lines1 + lines2

        def get_spread_line_id(last_spread_line):
            spread_line_id = last_spread_line and last_spread_line.id
            return spread_line_id

        SpreadLine = self.env['account.invoice.spread.line']
        digits = self.env['decimal.precision'].precision_get('Account')

        if self.price_subtotal == 0.0:
            return
        domain = [
            ('invoice_line_id', '=', self.id),
            ('type', '=', 'spread'),
            ('move_id', '!=', False)]

        posted_spreads = SpreadLine.search(domain, order='line_date desc')
        last_spread_line = get_last_spread_line(posted_spreads)

        domain = [
            ('invoice_line_id', '=', self.id),
            ('type', '=', 'depreciate'),
            ('move_id', '=', False)]

        old_spreads = SpreadLine.search(domain)
        old_spreads.unlink()

        table = self._compute_spread_table()
        if not table:
            return

        # group lines prior to spread start period
        spread_start_date = get_format_date(self.spread_start_date)
        total_lines = compute_lines(spread_start_date, table)
        table[0]['lines'] = total_lines

        # check table with posted entries and
        # recompute in case of deviation
        table_i_start = 0
        line_i_start = 0
        if posted_spreads:
            residual_amount_table = 0.0
            last_spread_date = datetime.strptime(
                last_spread_line.line_date, '%Y-%m-%d')
            last_date_in_table = table[-1]['lines'][-1]['date']
            if last_date_in_table <= last_spread_date:
                raise Warning(
                    _('Error!'),
                    _("The duration of the spread conflicts with the "
                      "posted spread table entry dates."))

            for table_i, entry in enumerate(table):
                residual_amount_table = \
                    entry['lines'][-1]['remaining_value']
                if entry['date_start'] <= last_spread_date \
                        <= entry['date_stop']:
                    break
            if entry['date_stop'] == last_spread_date:
                table_i += 1
                line_i = 0
            else:
                entry = table[table_i]
                date_min = entry['date_start']
                for line_i, line in enumerate(entry['lines']):
                    residual_amount_table = line['remaining_value']
                    if date_min <= last_spread_date <= line['date']:
                        break
                    date_min = line['date']
                if line['date'] == last_spread_date:
                    line_i += 1
            table_i_start = table_i
            line_i_start = line_i

            # check if residual value corresponds with table
            # and adjust table when needed
            spreaded_value = 0.0
            for posted_spread in posted_spreads:
                spreaded_value += posted_spread.amount

            residual_amount = self.price_subtotal - spreaded_value
            amount_diff = round(
                residual_amount_table - residual_amount, digits)
            if amount_diff:
                entry = table[table_i_start]
                fy_amount_check = 0.0

                # TODO remove code here
                if entry['fy_id']:
                    fy_amount_check = 0.0
                    for posted_spread in posted_spreads:
                        line_date = posted_spread.line_date
                        if line_date >= entry['date_start']:
                            if line_date <= entry['date_stop']:
                                fy_amount_check += posted_spread.amount

                lines = entry['lines']
                for line in lines[line_i_start:-1]:
                    line['spreaded_value'] = spreaded_value
                    spreaded_value += line['amount']
                    fy_amount_check += line['amount']
                    residual_amount -= line['amount']
                    line['remaining_value'] = residual_amount
                lines[-1]['spreaded_value'] = spreaded_value
                lines[-1]['amount'] = entry['fy_amount'] - fy_amount_check

        seq = len(posted_spreads)
        spread_line_id = get_spread_line_id(last_spread_line)
        last_date = table[-1]['lines'][-1]['date']
        for entry in table[table_i_start:]:
            for line in entry['lines'][line_i_start:]:
                seq += 1
                name = self._get_spread_entry_name(seq)
                if line['date'] == last_date:
                    # ensure that the last entry of the table always
                    # depreciates the remaining value
                    existing_amount = 0.0
                    for existspread in SpreadLine.search(
                            [('line_date', '<', last_date),
                             ('invoice_line_id', '=', self.id)]):
                        existing_amount += existspread.amount

                    amount = self.price_subtotal - existing_amount
                else:
                    amount = line['amount']
                previous_id = get_spread_line_id(spread_line_id)
                vals = {
                    'previous_id': previous_id,
                    'amount': amount,
                    'invoice_line_id': self.id,
                    'name': name,
                    'line_date': line['date'].strftime('%Y-%m-%d'),
                }
                spread_line_id = SpreadLine.create(vals)
            line_i_start = 0

    @api.multi
    def compute_spread_board(self):
        for line in self:
            line._compute_spread_board()
