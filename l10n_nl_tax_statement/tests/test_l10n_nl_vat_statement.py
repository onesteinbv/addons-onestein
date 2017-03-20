# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo import fields
from odoo.tests.common import TransactionCase


class TestVatStatement(TransactionCase):

    def test_01_statement_defaults(self):

        # create tax statement
        company = self.env.user.company_id
        statement = self.env['l10n.nl.vat.statement'].create({})

        # check default values
        fy_dates = company.compute_fiscalyear_dates(datetime.now())
        from_date = fields.Date.to_string(fy_dates['date_from'])
        to_date = fields.Date.to_string(fy_dates['date_to'])
        self.assertEquals(statement.from_date, from_date)
        self.assertEquals(statement.to_date, to_date)
        self.assertEquals(statement.company_id, company)
        self.assertEquals(statement.name, company.name)

    def test_02_statement_lines(self):
        tax_account_id = self.env['account.account'].search(
            [('name', '=', 'Tax Paid')], limit=1).id
        tax = self.env['account.tax'].create({
            'name': 'Tax 21.0%',
            'amount': 21.0,
            'amount_type': 'percent',
            'account_id': tax_account_id,
        })
        invoice_account_id = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_receivable'
            ).id)], limit=1).id
        invoice_line_account_id = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_expenses').id)], limit=1).id

        # create invoice
        invoice = self.env['account.invoice'].create({
            'partner_id': self.env.ref('base.res_partner_2').id,
            'account_id': invoice_account_id,
            'type': 'out_invoice',
        })
        self.env['account.invoice.line'].create({
            'product_id': self.env.ref('product.product_product_4').id,
            'quantity': 1.0,
            'price_unit': 100.0,
            'invoice_id': invoice.id,
            'name': 'product that costs 100',
            'account_id': invoice_line_account_id,
            'invoice_line_tax_ids': [(6, 0, [tax.id])],
        })
        invoice._onchange_invoice_line_ids()
        invoice._convert_to_write(invoice._cache)
        self.assertEqual(invoice.state, 'draft')

        # validate invoice
        invoice.action_invoice_open()

        self.assertEquals(tax.base_balance, 100.)
        self.assertEquals(tax.balance, 21.)
        self.assertEquals(tax.base_balance_regular, 100.)
        self.assertEquals(tax.balance_regular, 21.)
        self.assertEquals(tax.base_balance_refund, 0.)
        self.assertEquals(tax.balance_refund, 0.)

        # create tax statement
        statement = self.env['l10n.nl.vat.statement'].create({})

        # calculate lines
        statement.update()
