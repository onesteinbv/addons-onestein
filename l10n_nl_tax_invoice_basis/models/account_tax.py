# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def get_move_line_partial_domain(self, from_date, to_date, company_id):
        res = super(AccountTax, self).get_move_line_partial_domain(
            from_date,
            to_date,
            company_id
        )
        if not self._context.get('skip_invoice_basis_domain'):
            company = self.env['res.company'].browse(company_id)
            is_nl = company.country_id == self.env.ref('base.nl')
            if is_nl:
                domain_params = {
                    'company_id': company_id,
                    'from_date': from_date,
                    'to_date': to_date,
                }
                # following line breaks the inheritance chain;
                # it is intentional, to avoid other modules to interfere;
                # pass context ''skip_invoice_basis_domain' if you
                # don't want to allow this behavior
                res = self._get_invoice_basis_domain(domain_params)
        return res

    def _get_invoice_basis_domain(self, domain_params):
        tax_date_domain = self._get_tax_date_domain(domain_params)
        date_domain = self._get_accounting_date_domain(domain_params)
        return [
            ('company_id', '=', domain_params['company_id']),
            '|',
        ] + tax_date_domain + date_domain

    def _get_accounting_date_domain(self, domain_params):
        # if 'l10n_nl_date_invoice' is not set, get the account date instead
        return [
            '&', '&',
            ('l10n_nl_date_invoice', '=', False),
            ('date', '>=', domain_params['from_date']),
            ('date', '<=', domain_params['to_date']),
        ]

    def _get_tax_date_domain(self, domain_params):
        # if 'l10n_nl_date_invoice' is set, use this value
        # instead of the standard 'date'
        return [
            '&', '&',
            ('l10n_nl_date_invoice', '!=', False),
            ('l10n_nl_date_invoice', '>=', domain_params['from_date']),
            ('l10n_nl_date_invoice', '<=', domain_params['to_date']),
        ]
