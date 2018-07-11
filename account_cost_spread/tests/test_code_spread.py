# -*- coding: utf-8 -*-
# Copyright 2017-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.account.tests.account_test_classes import AccountingTestCase
from odoo.exceptions import UserError


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

        self.partner = self.env['res.partner'].create({
            'name': 'Partner Name',
            'supplier': True,
        })
        self.invoice = self.env['account.invoice'].with_context(
            default_type='in_invoice'
        ).create({
            'partner_id': self.partner.id,
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

        self.invoice_2 = self.env['account.invoice'].with_context(
            default_type='in_invoice'
        ).create({
            'partner_id': self.partner.id,
            'account_id': self.invoice_account.id,
            'type': 'in_invoice',
        })
        self.invoice_line_2 = self.env['account.invoice.line'].create({
            'quantity': 1.0,
            'price_unit': 1000.0,
            'invoice_id': self.invoice_2.id,
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
        self.assertEqual(83.33, self.invoice_line.spread_line_ids[0].amount)
        self.assertEqual(83.33, self.invoice_line.spread_line_ids[1].amount)
        self.assertEqual(83.33, self.invoice_line.spread_line_ids[2].amount)
        self.assertEqual(83.33, self.invoice_line.spread_line_ids[3].amount)
        self.assertEqual(83.33, self.invoice_line.spread_line_ids[4].amount)
        self.assertEqual(83.33, self.invoice_line.spread_line_ids[5].amount)
        self.assertEqual(83.33, self.invoice_line.spread_line_ids[6].amount)
        self.assertEqual(83.33, self.invoice_line.spread_line_ids[7].amount)
        self.assertEqual(83.33, self.invoice_line.spread_line_ids[8].amount)
        self.assertEqual(83.33, self.invoice_line.spread_line_ids[9].amount)
        self.assertEqual(83.33, self.invoice_line.spread_line_ids[10].amount)
        self.assertEqual(83.37, self.invoice_line.spread_line_ids[11].amount)

        # Cancel the account move which is in posted state
        # and verifies that it gives warning message
        with self.assertRaises(UserError):
            self.invoice.move_id.button_cancel()

    def test_02_supplier_invoice(self):
        # date invoice set
        self.invoice.date_invoice = '2017-03-01'
        self.invoice_line.write({
            'price_unit': 2000.0,
            'name': 'product that cost 2000',
            'period_number': 7,
            'period_type': 'quarter',
            'spread_date': None
        })

        # change the state of invoice to open by clicking Validate button
        self.invoice.action_invoice_open()

        self.assertEqual(len(self.invoice_line.spread_line_ids), 7)
        self.assertEqual(285.71, self.invoice_line.spread_line_ids[0].amount)
        self.assertEqual(285.71, self.invoice_line.spread_line_ids[1].amount)
        self.assertEqual(285.71, self.invoice_line.spread_line_ids[2].amount)
        self.assertEqual(285.71, self.invoice_line.spread_line_ids[3].amount)
        self.assertEqual(285.71, self.invoice_line.spread_line_ids[4].amount)
        self.assertEqual(285.71, self.invoice_line.spread_line_ids[5].amount)
        self.assertEqual(285.74, self.invoice_line.spread_line_ids[6].amount)
        total_line_amount = 0.0
        for line in self.invoice_line.spread_line_ids:
            total_line_amount += line.amount
        self.assertLessEqual(abs(total_line_amount - 2000.0), 0.0001)

        # simulate the click on the arrow that displays the spread details
        details = self.invoice_line.spread_details()
        self.assertEqual(details['res_id'], self.invoice_line.id)

    def test_03_supplier_invoice(self):
        # no date set
        self.invoice_line.write({
            'quantity': 1.0,
            'price_unit': 1000.0,
            'invoice_id': self.invoice.id,
            'name': 'product that cost 1000',
            'account_id': self.invoice_line_account.id,
            'spread_account_id': self.spread_account,
            'period_number': 3,
            'period_type': 'year',
            'spread_date': None
        })
        self.invoice.write({'date_invoice': None})
        self.invoice_line._compute_spread_start_date()

        # change the state of invoice to open by clicking Validate button
        self.invoice.action_invoice_open()

        self.assertEqual(len(self.invoice_line.spread_line_ids), 4)
        self.assertEqual(333.33, self.invoice_line.spread_line_ids[1].amount)
        self.assertEqual(333.33, self.invoice_line.spread_line_ids[2].amount)
        first_amount = self.invoice_line.spread_line_ids[0].amount
        last_amount = self.invoice_line.spread_line_ids[3].amount
        remaining_amount = first_amount + last_amount
        self.assertLessEqual(abs(remaining_amount - 333.34), 0.0001)
        total_line_amount = 0.0
        for line in self.invoice_line.spread_line_ids:
            total_line_amount += line.amount
        self.assertLessEqual(abs(total_line_amount - 1000.0), 0.0001)

    def test_04_supplier_invoice(self):
        # spread date set
        self.invoice_line.write({
            'period_number': 12,
            'period_type': 'month',
            'spread_date': '2017-02-01'
        })

        # change the state of invoice to open by clicking Validate button
        self.invoice.action_invoice_open()

        # create moves for all the spread lines and open them
        self.invoice_line.spread_line_ids.create_moves()
        for spread_line in self.invoice_line.spread_line_ids:
            attrs = spread_line.open_move()
            self.assertEqual(isinstance(attrs, dict), True)

        # post and then unlink all created moves
        self.invoice.journal_id.write({'update_posted': True})
        for line in self.invoice_line.spread_line_ids:
            line.move_id.post()
        self.invoice_line.spread_line_ids.unlink_move()
        for spread_line in self.invoice_line.spread_line_ids:
            self.assertEqual(len(spread_line.move_id), 0)

    def test_05_supplier_invoice(self):
        # spread date set
        self.invoice_line.write({
            'period_number': 8,
            'period_type': 'month'
        })

        # change the state of invoice to open by clicking Validate button
        self.invoice.action_invoice_open()

        # create moves for all the spread lines and open them
        self.invoice_line.spread_line_ids.create_moves()

        # check move lines
        for spread_line in self.invoice_line.spread_line_ids:
            for move_line in spread_line.move_id.line_ids:
                spread_account = self.invoice_line.spread_account_id
                if move_line.account_id == spread_account:
                    self.assertEqual(move_line.credit, spread_line.amount)

    def test_06_supplier_invoice(self):
        # spread date set
        self.invoice_line.write({
            'price_unit': 345.96,
            'period_number': 3,
            'period_type': 'month',
            'spread_date': '2017-01-01'
        })
        self.invoice.write({
            'date_invoice': '2016-12-31'
        })
        # change the state of invoice to open by clicking Validate button
        self.invoice.action_invoice_open()
        self.assertEqual(len(self.invoice_line.spread_line_ids), 3)
        self.assertEqual(115.32,
                         self.invoice_line.spread_line_ids[0].amount)
        self.assertEqual('2017-01-31',
                         self.invoice_line.spread_line_ids[0].line_date)
        self.assertEqual(115.32,
                         self.invoice_line.spread_line_ids[1].amount)
        self.assertEqual('2017-02-28',
                         self.invoice_line.spread_line_ids[1].line_date)
        self.assertEqual(115.32,
                         self.invoice_line.spread_line_ids[2].amount)
        self.assertEqual('2017-03-31',
                         self.invoice_line.spread_line_ids[2].line_date)

    def test_07_supplier_invoice(self):
        # spread date set
        self.invoice_line.write({
            'period_number': 12,
            'period_type': 'month',
            'spread_date': '2017-02-01'
        })
        self.assertTrue(self.invoice_line.is_all_set_for_spread())

        # change the state of invoice to open by clicking Validate button
        self.invoice.action_invoice_open()
        self.invoice.journal_id.write({'update_posted': True})
        self.invoice.action_invoice_cancel()
        self.assertEqual(len(self.invoice_line.spread_line_ids), 0)

    def test_08_supplier_invoice(self):
        # spread date set
        self.invoice_line.write({
            'period_number': 12,
            'period_type': 'month',
            'spread_date': '2017-02-01'
        })
        self.assertTrue(self.invoice_line.is_all_set_for_spread())

        # change the state of invoice to open by clicking Validate button
        self.invoice.action_invoice_open()
        self.invoice.journal_id.write({'update_posted': True})
        self.invoice.action_invoice_cancel()
        self.assertEqual(len(self.invoice_line.spread_line_ids), 0)

    def test_09_not_compute_spread_board(self):
        self.invoice_line.write({
            'spread_account_id': False,
        })
        self.assertFalse(self.invoice_line.is_all_set_for_spread())
        self.invoice_line.compute_spread_board()
        self.assertEqual(len(self.invoice_line.spread_line_ids), 0)

    def test_10_compute_spread_board(self):
        self.invoice_line.account_id.write({
            'deprecated': True,
        })
        self.assertTrue(self.invoice_line.is_all_set_for_spread())
        with self.assertRaises(UserError):
            self.invoice_line.compute_spread_board()

    def test_11_create_entries(self):
        self.env['account.invoice.spread.line']._create_entries()

    def test_12_create_move_in_invoice(self):
        self.invoice_2.action_invoice_open()
        self.invoice_line_2.spread_line_ids.create_moves()
