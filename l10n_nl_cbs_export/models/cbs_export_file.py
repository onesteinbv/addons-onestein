# -*- coding: utf-8 -*-
# Copyright 2017 Odoo Experts (<https://www.odooexperts.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import calendar
import time
import logging
from datetime import datetime, date, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CbsExportFile(models.Model):
    _name = 'cbs.export.file'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.multi
    def _compute_get_filename(self):
        for rec in self:
            rec.filename = '%s_%s.csv' % (rec.month, rec.year)

    @api.multi
    def _default_get_month(self):
        context_today = fields.Date.context_today(self)
        return fields.Date.from_string(context_today).strftime('%m')

    @api.model
    def _default_get_year(self):
        context_today = fields.Date.context_today(self)
        return fields.Date.from_string(context_today).strftime('%Y')

    cbs_export_invoice = fields.Binary(
        string='CBS Export File',
        attachment=True
    )
    filename = fields.Char(compute='_compute_get_filename')
    name = fields.Char()
    month = fields.Selection([
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')
    ], required=True, default=_default_get_month)
    year = fields.Char(size=4, required=True, default=_default_get_year)
    account_invoice_ids = fields.One2many('account.invoice', 'cbs_export_id')
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        readonly=True,
        default=lambda self: self.env.user.company_id
    )

    _sql_constraints = [(
        'month_year_company_unique',
        'unique(month, year, company_id)',
        _('A CBS export already exists with the same month and year '
          'for this company!')
        )]

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('cbs.export.file')
        return super(CbsExportFile, self).create(vals)

    @api.multi
    def get_data(self):
        self.ensure_one()
        invoices = self.set_invoice()
        if not invoices:
            raise ValidationError(
                _("There are no invoice lines for CBS Export "
                  "during month %s in year %s") % (
                    calendar.month_name[int(self.month)], self.year
                )
            )
        self.export_file()

    @api.constrains('year')
    def check_year(self):
        if self.year:
            if not self.year.isdigit():
                raise ValidationError(_("Please insert a valid Year"))

            is_valid_year = '%d' % (int(self.year))
            try:
                time.strptime(is_valid_year, '%Y')
            except ValueError:
                raise ValidationError(_("Please insert a valid Year"))

    @api.multi
    def set_invoice(self):
        self.ensure_one()
        days = calendar.monthrange(int(self.year), int(self.month))
        invoices = self.env['account.invoice'].search([
            ('type', '=', 'out_invoice'),
            ('state', 'in', ['open', 'paid']),
            ('company_id', '=', self.company_id.id),
            ('partner_id.country_id.intrastat', '=', True),
            ('partner_id.country_id.code', '!=', 'NL'),
            ('date_invoice', '>=', datetime.strptime(
                '%s-%s-%s' % (
                    1, int(self.month), int(self.year)
                ), '%d-%m-%Y')
             ),
            ('date_invoice', '<=', datetime.strptime(
                '%s-%s-%s' % (
                    days[1], int(self.month), int(self.year)
                ), '%d-%m-%Y'))]
        )
        if invoices:
            self.env['account.invoice'].search([
                ('cbs_export_id', '=', self.id),
                ('company_id', '=', self.company_id.id),
                ('id', 'not in', invoices.ids)
            ]).write(
                {'cbs_export_id': False}
            )
            invoices.write({'cbs_export_id': self.id})
        return invoices

    @api.model
    def cron_get_cbs_export_file(self):
        last_month = date.today().replace(day=1) - timedelta(days=1)
        companies = self.env['res.company'].search([])
        for company in companies:
            cbs_export_file = self.search([
                ('month', '=', last_month.strftime("%m")),
                ('year', '=', last_month.strftime("%Y")),
                ('company_id', '=', company.id)
            ], limit=1)
            if not cbs_export_file:
                cbs_export_file = self.create({
                    'month': last_month.strftime("%m"),
                    'year': last_month.strftime("%Y"),
                    'company_id': company.id
                })
            invoices = cbs_export_file.set_invoice()
            if not invoices:
                _logger.info(
                    "There are no invoice lines for CBS Export "
                    "during month %s in year %s",
                    calendar.month_name[int(cbs_export_file.month)],
                    cbs_export_file.year
                )
            else:
                cbs_export_file.export_file()

    @api.multi
    def export_file(self):
        self.ensure_one()

        cbs_export_data = self._format_header()
        cbs_export_data += self._format_lines()
        cbs_export_data += self._format_footer()

        self.message_post(
            body=_("CBS Export is created for month %s in year %s") % (
                calendar.month_name[int(self.month)],
                self.year
            ),
            subtype='mt_comment'
        )
        self.cbs_export_invoice = base64.encodestring(cbs_export_data)

    @api.model
    def _format_header(self):
        company = self.company_id

        cbs_export_data = \
            str('9801') + \
            str(company.vat or '').replace(' ', '')[2:].ljust(12) + \
            str(datetime.now().strftime("%Y%m").ljust(6)) + \
            str(company.name or '').ljust(40) + \
            str(" " * 6) + \
            str(" " * 5) + \
            str(datetime.now().strftime("%Y%m%d").ljust(8)) + \
            str(datetime.now().strftime("%H%M%S").ljust(6)) + \
            str(company.phone or '').replace(' ', '')[0:15].ljust(15) + \
            str(" " * 13) + '\n'

        return cbs_export_data

    @api.model
    def _format_footer(self):
        cbs_export_data = str('9899') + str(" " * 111)
        return cbs_export_data

    @api.multi
    def _format_lines(self):
        self.ensure_one()

        line_counter = 1
        cbs_export_data = ''
        invoices = self.account_invoice_ids

        for invoice_line in invoices.mapped('invoice_line_ids'):
            sign_of_weight = '-'
            sign_of_invoice_value = '-'
            if invoice_line.invoice_id.amount_total_signed >= 0:
                sign_of_invoice_value = '+'
            if (invoice_line.quantity * invoice_line.product_id.weight) >= 0:
                sign_of_weight = '+'

            value = \
                str(datetime.strptime(
                    invoice_line.invoice_id.date_invoice, '%Y-%m-%d'
                ).strftime("%Y%m") or '').ljust(6) + \
                str('7') + \
                str(invoice_line.company_id.vat or ''
                    ).replace(' ', '')[2:].ljust(12) + \
                str(line_counter).zfill(5) + str(" " * 3) + \
                str(invoice_line.invoice_id.partner_id.country_id.code or ''
                    ).ljust(3) + \
                str('3') + \
                str('0') + \
                str('00') + \
                str('00') + \
                str('1') + \
                str(invoice_line.product_id.intrastat_id.name or ''
                    ).replace(' ', '')[0:8].ljust(8) + \
                str('00') + \
                str(sign_of_weight) + \
                str(int(invoice_line.quantity * invoice_line.product_id.weight)
                    ).zfill(10) + \
                str('+') + \
                str('0000000000').zfill(10) + sign_of_invoice_value + \
                str(int(invoice_line.price_subtotal)).zfill(10) + \
                str('+') + \
                str('0000000000').zfill(10)

            if len(str(invoice_line.invoice_id.number or '')) < 8:
                invoice_value = \
                    str(invoice_line.invoice_id.number) + \
                    str(line_counter).zfill(2)
                value += str(invoice_value).ljust(10)
            else:
                value += str(
                    invoice_line.invoice_id.number or ' '
                )[:8].ljust(8) + str(line_counter).zfill(2)

            value += \
                str(" " * 3) + \
                str(" " * 1) + \
                str('000') + \
                str(" " * 7) + '\n'

            line_counter += 1
            cbs_export_data += value

        return cbs_export_data
