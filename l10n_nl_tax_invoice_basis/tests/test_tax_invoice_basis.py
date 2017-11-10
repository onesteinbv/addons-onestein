# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestTaxInvoiceBasis(TransactionCase):

    def setUp(self):
        super(TestTaxInvoiceBasis, self).setUp()
        self.env.user.company_id.country_id = self.env.ref('base.nl')

        tax_account_id = self.env['account.account'].search(
            [('name', '=', 'Tax Paid')], limit=1).id
        self.tax = self.env['account.tax'].create({
            'name': 'Tax 21.0%',
            'amount': 21.0,
            'amount_type': 'percent',
            'account_id': tax_account_id,
        })
        receivable_account_id = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_receivable'
            ).id)], limit=1).id
        invoice = self.env['account.invoice'].create({
            'partner_id': self.env.ref('base.res_partner_4').id,
            'account_id': receivable_account_id,
            'date_invoice': '2017-08-18',
            'date': '2017-07-01',
            'type': 'in_invoice',
        })
        invoice_line_account_id = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_expenses').id)], limit=1).id
        self.env['account.invoice.line'].create({
            'invoice_id': invoice.id,
            'product_id': self.env.ref('product.product_product_4').id,
            'name': 'product that cost 100',
            'account_id': invoice_line_account_id,
            'quantity': 1.0,
            'price_unit': 100.0,
            'invoice_line_tax_ids': [(6, 0, [self.tax.id])],
        })
        invoice._onchange_invoice_line_ids()
        invoice._convert_to_write(invoice._cache)

        self.period_july = {
            'from_date': '2017-07-01',
            'to_date': '2017-07-31',
        }
        self.period_august = {
            'from_date': '2017-08-01',
            'to_date': '2017-08-31',
        }
        self.invoice = invoice

    def test_tax_invoice_basis(self):

        company = self.env.user.company_id
        # Factuurstelsel enabled by default
        self.assertEquals(company.l10n_nl_tax_invoice_basis, True)

        # Validate invoice
        self.invoice.action_invoice_open()

        tax_july = self.tax.with_context(self.period_july)
        tax_august = self.tax.with_context(self.period_august)

        self.assertEquals(tax_july.base_balance, 0.)
        self.assertEquals(tax_july.balance, 0.)
        self.assertEquals(tax_july.base_balance_regular, 0.)
        self.assertEquals(tax_july.balance_regular, 0.)
        self.assertEquals(tax_july.base_balance_refund, 0.)
        self.assertEquals(tax_july.balance_refund, 0.)

        self.assertEquals(tax_august.base_balance, -100.)
        self.assertEquals(tax_august.balance, -21.)
        self.assertEquals(tax_august.base_balance_regular, 0.)
        self.assertEquals(tax_august.balance_regular, 0.)
        self.assertEquals(tax_august.base_balance_refund, -100.)
        self.assertEquals(tax_august.balance_refund, -21.)

    def test_tax_standard(self):

        # Factuurstelsel disabled
        self.env.user.company_id.l10n_nl_tax_invoice_basis = False

        # Validate invoice
        self.invoice.action_invoice_open()

        tax_july = self.tax.with_context(self.period_july)
        tax_august = self.tax.with_context(self.period_august)

        self.assertEquals(tax_july.base_balance, -100.)
        self.assertEquals(tax_july.balance, -21.)
        self.assertEquals(tax_july.base_balance_regular, 0.)
        self.assertEquals(tax_july.balance_regular, 0.)
        self.assertEquals(tax_july.base_balance_refund, -100.)
        self.assertEquals(tax_july.balance_refund, -21.)

        self.assertEquals(tax_august.base_balance, 0.)
        self.assertEquals(tax_august.balance, 0.)
        self.assertEquals(tax_august.base_balance_regular, 0.)
        self.assertEquals(tax_august.balance_regular, 0.)
        self.assertEquals(tax_august.base_balance_refund, 0.)
        self.assertEquals(tax_august.balance_refund, 0.)

    def test_skip_by_context(self):

        # Factuurstelsel configured as enabled
        # but context is used to skip the functionality
        update_ctx = {'skip_invoice_basis_domain': True}
        self.period_july.update(update_ctx)
        self.period_august.update(update_ctx)

        # Validate invoice
        self.invoice.action_invoice_open()

        tax_july = self.tax.with_context(self.period_july)
        tax_august = self.tax.with_context(self.period_august)

        self.assertEquals(tax_july.base_balance, -100.)
        self.assertEquals(tax_july.balance, -21.)
        self.assertEquals(tax_july.base_balance_regular, 0.)
        self.assertEquals(tax_july.balance_regular, 0.)
        self.assertEquals(tax_july.base_balance_refund, -100.)
        self.assertEquals(tax_july.balance_refund, -21.)

        self.assertEquals(tax_august.base_balance, 0.)
        self.assertEquals(tax_august.balance, 0.)
        self.assertEquals(tax_august.base_balance_regular, 0.)
        self.assertEquals(tax_august.balance_regular, 0.)
        self.assertEquals(tax_august.base_balance_refund, 0.)
        self.assertEquals(tax_august.balance_refund, 0.)
