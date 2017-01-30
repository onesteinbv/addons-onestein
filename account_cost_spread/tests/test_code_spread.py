# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.account.tests.account_test_classes import AccountingTestCase
from odoo.exceptions import Warning


class TestAccountCostSpread(AccountingTestCase):

    def setUp(self):
        super(TestAccountCostSpread, self).setUp()
        receivable = self.env.ref('account.data_account_type_receivable')
        expenses = self.env.ref('account.data_account_type_expenses')

        self.invoice_account = self.env['account.account'].search([
            ('user_type_id', '=', receivable.id)
        ], limit=1).id
        self.invoice_line_account = self.env['account.account'].search([
            ('user_type_id', '=', expenses.id)
        ], limit=1).id
        self.spread_account = self.env['account.account'].search([
            ('user_type_id', '=', expenses.id),
            ('id', '!=', self.invoice_line_account)
        ], limit=1).id

        self.vendor = self.env['res.partner'].create({
            'name': 'Vendor1',
            'supplier': True,
        })

    def test_01_supplier_invoice(self):
        invoice = self.env['account.invoice'].create({
            'partner_id': self.vendor.id,
            'account_id': self.invoice_account,
            'type': 'in_invoice',
        })
        invoice_line = self.env['account.invoice.line'].create({
            'quantity': 1.0,
            'price_unit': 1000.0,
            'invoice_id': invoice.id,
            'name': 'product that cost 1000',
            'account_id': self.invoice_line_account,
            'spread_account_id': self.spread_account,
            'period_number': 12,
            'period_type': 'month',
            'spread_date': '2017-02-01'
        })

        # change the state of invoice to open by clicking Validate button
        invoice.action_invoice_open()
        self.assertEqual(len(invoice_line.spread_line_ids), 12)
        self.assertEqual(81.77, invoice_line.spread_line_ids[0].amount)
        self.assertEqual(83.33, invoice_line.spread_line_ids[1].amount)
        self.assertEqual(83.33, invoice_line.spread_line_ids[2].amount)
        self.assertEqual(83.33, invoice_line.spread_line_ids[3].amount)
        self.assertEqual(83.33, invoice_line.spread_line_ids[4].amount)
        self.assertEqual(83.33, invoice_line.spread_line_ids[5].amount)
        self.assertEqual(83.33, invoice_line.spread_line_ids[6].amount)
        self.assertEqual(83.33, invoice_line.spread_line_ids[7].amount)
        self.assertEqual(83.33, invoice_line.spread_line_ids[8].amount)
        self.assertEqual(83.33, invoice_line.spread_line_ids[9].amount)
        self.assertEqual(83.33, invoice_line.spread_line_ids[10].amount)
        self.assertEqual(84.93, invoice_line.spread_line_ids[11].amount)

        # Cancel the account move which is in posted state
        # and verifies that it gives warning message
        with self.assertRaises(Warning):
            invoice.move_id.button_cancel()

    def test_02_supplier_invoice(self):
        invoice = self.env['account.invoice'].create({
            'partner_id': self.vendor.id,
            'account_id': self.invoice_account,
            'type': 'in_invoice',
            'date_invoice': '2017-03-01'
        })
        invoice_line = self.env['account.invoice.line'].create({
            'quantity': 1.0,
            'price_unit': 2000.0,
            'invoice_id': invoice.id,
            'name': 'product that cost 2000',
            'account_id': self.invoice_line_account,
            'spread_account_id': self.spread_account,
            'period_number': 7,
            'period_type': 'quarter',
            'spread_date': None
        })

        # change the state of invoice to open by clicking Validate button
        invoice.action_invoice_open()
        self.assertEqual(len(invoice_line.spread_line_ids), 8)
        self.assertEqual(100.96, invoice_line.spread_line_ids[0].amount)
        self.assertEqual(285.72, invoice_line.spread_line_ids[1].amount)
        self.assertEqual(285.72, invoice_line.spread_line_ids[2].amount)
        self.assertEqual(285.72, invoice_line.spread_line_ids[3].amount)
        self.assertEqual(285.72, invoice_line.spread_line_ids[4].amount)
        self.assertEqual(285.72, invoice_line.spread_line_ids[5].amount)
        self.assertEqual(285.72, invoice_line.spread_line_ids[6].amount)
        self.assertEqual(184.72, invoice_line.spread_line_ids[7].amount)

        # simulate the click on the arrow that displays the spead details
        details = invoice_line.spread_details()
        self.assertEqual(details['res_id'], invoice_line.id)

    def test_03_supplier_invoice(self):
        invoice = self.env['account.invoice'].create({
            'partner_id': self.vendor.id,
            'account_id': self.invoice_account,
            'type': 'in_invoice',
            'date_invoice': None
        })
        invoice_line = self.env['account.invoice.line'].create({
            'quantity': 1.0,
            'price_unit': 1000.0,
            'invoice_id': invoice.id,
            'name': 'product that cost 1000',
            'account_id': self.invoice_line_account,
            'spread_account_id': self.spread_account,
            'period_number': 3,
            'period_type': 'quarter',
            'spread_date': None
        })

        # change the state of invoice to open by clicking Validate button
        invoice.action_invoice_open()
        self.assertEqual(len(invoice_line.spread_line_ids), 4)
        total_line_amount = 0.0
        for line in invoice_line.spread_line_ids:
            total_line_amount += line.amount
        self.assertEqual(total_line_amount, 1000.0)
