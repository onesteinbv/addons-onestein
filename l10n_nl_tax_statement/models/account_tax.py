# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def get_move_line_partial_domain(self, from_date, to_date, company_id):

        res = super(AccountTax, self).get_move_line_partial_domain(
            from_date,
            to_date,
            company_id
        )

        if self._context.get('skip_invoice_basis_domain'):
            company = self.env['res.company'].browse(company_id)
            is_nl = company.country_id == self.env.ref('base.nl')
            if is_nl:
                res = [
                    ('company_id', '=', company_id),
                    ('l10n_nl_vat_statement_id', '=', False),
                    ('l10n_nl_vat_statement_include', '=', True),
                ]
                res += self._get_move_line_tax_date_range_domain(from_date)
        return res

    @api.model
    def _get_move_line_tax_date_range_domain(self, from_date):
        unreported_from_date = self._context.get('unreported_move_from_date')
        if self._context.get('is_invoice_basis'):
            if unreported_from_date:
                res = [
                    '|',
                    '&', '&',
                    ('l10n_nl_date_invoice', '=', False),
                    ('date', '<', from_date),
                    ('date', '>=', unreported_from_date),
                    '&', '&',
                    ('l10n_nl_date_invoice', '!=', False),
                    ('l10n_nl_date_invoice', '<', from_date),
                    ('l10n_nl_date_invoice', '>=', unreported_from_date),
                ]
            else:
                res = [
                    '|',
                    '&',
                    ('l10n_nl_date_invoice', '=', False),
                    ('date', '<', from_date),
                    '&',
                    ('l10n_nl_date_invoice', '!=', False),
                    ('l10n_nl_date_invoice', '<', from_date),
                ]
        else:
            res = [
                ('date', '<', from_date),
            ]
            if unreported_from_date:
                res += [
                    ('date', '>=', unreported_from_date),
                ]
        return res
