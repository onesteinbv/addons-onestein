# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.account.tests.account_test_classes import AccountingTestCase


class TestAccountCostSpread(AccountingTestCase):

    def setUp(self):
        super(TestAccountCostSpread, self).setUp()
        receivable = self.env.ref('account.data_account_type_receivable')
        expenses = self.env.ref('account.data_account_type_expenses')

        def get_account(obj):
            res = self.env['account.account'].search([
                ('user_type_id', '=', obj.id)
            ], limit=1)
            return res

        self.invoice_account = get_account(receivable)
        self.invoice_line_account = get_account(expenses)

        self.spread_account = self.env['account.account'].search([
            ('user_type_id', '=', expenses.id),
            ('id', '!=', self.invoice_line_account.id)
        ], limit=1).id

        self.vendor = self.env['res.partner'].create({
            'name': 'Vendor1',
            'supplier': True,
        })
        self.invoice = self.env['account.invoice'].create({
            'partner_id': self.vendor.id,
            'account_id': self.invoice_account.id,
            'type': 'in_invoice',
        })
        self.invoice_line = self.env['account.invoice.line'].create({
            'quantity': 1.0,
            'price_unit': 1000.0,
            'invoice_id': self.invoice.id,
            'name': 'product that cost 1000',
            'account_id': self.invoice_line_account.id,
            'spread_account_id': self.spread_account,
            'period_number': 12,
            'period_type': 'month',
            'spread_date': '2017-02-01'
        })

    def test_01_supplier_invoice(self):
        # spread date set
        self.invoice_line.write({
            'period_number': 12,
            'period_type': 'month',
            'spread_date': '2017-02-01'
        })

        # change the state of invoice to open by clicking Validate button
        self.invoice.action_invoice_open()
        self.assertEqual(len(self.invoice_line.spread_line_ids), 12)

        # create moves for all the spread lines
        self.invoice_line.create_all_moves()

        for spread_line in self.invoice_line.spread_line_ids:
            for move_line in spread_line.move_id.line_ids:
                spread_account = self.invoice_line.spread_account_id
                if move_line.account_id == spread_account:
                    self.assertEqual(move_line.credit, spread_line.amount)
