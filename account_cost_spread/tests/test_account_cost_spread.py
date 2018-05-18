# -*- coding: utf-8 -*-
# License AGPL-3.0 or later [http://www.gnu.org/licenses/agpl].

from openerp import fields
from openerp.tests.common import TransactionCase
from datetime import date


class TestAccountCostSpread(TransactionCase):

    def setUp(self):
        super(TestAccountCostSpread, self).setUp()

        # models for testing
        self.account_invoice_obj = self.env['account.invoice']
        self.account_invoice_line_obj = self.env['account.invoice.line']
        self.account_invoice_spread_line_obj = \
            self.env['account.invoice.spread.line']
        self.res_currency_obj = self.env['res.currency']

        # records for testing
        self.partner = self.env.ref('base.res_partner_2')
        self.currency_usd = self.env.ref("base.USD")
        self.account_fx_income = self.env.ref("account.income_fx_income")
        self.account_fx_expense = self.ref("account.income_fx_expense")
        self.bank_journal_usd = self.env.ref("account.bank_journal_usd")
        self.account_usd = self.env.ref("account.usd_bnk")
        self.product = self.env['product.product'].create({
            'name': 'product_demo',
            'type': 'service',
            'uos_id': self.env.ref('product.product_uom_categ_unit').id,
        })

    def test_all(self):
        # create invoice with test product and account
        today = date.today()
        invoice1 = self.account_invoice_obj.create({
            'account_id': self.account_fx_income.id,
            'company_id': self.partner.company_id.id,
            'currency_id': self.currency_usd.id,
            'invoice_line': [(0, 0, {
                'account_id': self.account_fx_income.id,
                'name': 'line1',
                'product_id': self.product.id,
                'quantity': 2000,
                'uos_id': self.product.uos_id.id,
                'price_unit': 33
            })],
            'journal_id': self.bank_journal_usd.id,
            'partner_id':  self.partner.id,
            'reference_type': 'none'
        })

        # confirm invoice
        invoice1.action_date_assign()
        invoice1.action_move_create()
        invoice1.action_number()
        invoice1.invoice_validate()
        self.assertEqual(invoice1.date_invoice, fields.Date.today())

        # create spread for this now confirmed invoice (if not confirmed it
        # would not have a date,
        # Make a spread on the line for the next 4 months
        # make invoice if the start date is intramonth the first spread  will
        # be proportionally less, the others will be equal, if there is some
        # left it will be added to an extra month. So in order to have exactly
        # 4 months we must impose start date to the beginning of the month.
        invoice1.invoice_line[0].write({
            'spread_account_id': self.account_fx_income.id,
            'period_number': 4,
            'period_type': 'month',
            'spread_date': fields.Date.to_string(today.replace(day=1))
        })

        # if the test is launched after september and the spread goes beyond 
        # current year we need to create new fiscalyear this year + 1
        self.next_fiscalyear = self.env['account.fiscalyear'].create({
            'name': 'thisyear',
            'code': 'THS',
            'company_id': 1,
            'date_start': fields.Date.to_string(
                today.replace(year=today.year+1, month=1, day=1)),
            'date_stop': fields.Date.to_string(
                today.replace(year=today.year+1, month=12, day=31))
        })

        # make period IDS for this fy
        self.next_fiscalyear.create_period()

        invoice1.invoice_line[0].action_recalculate_spread()
        self.assertEqual(len(invoice1.invoice_line.spread_line_ids), 4)
        # create move for every spread
        moves = []
        for spread_line in invoice1.invoice_line.spread_line_ids:
            moves += spread_line.create_move()
        # account cannot be reconciled
        for move in self.env['account.move'].browse(moves):
            for line in move.line_id:
                self.assertEqual(bool(line.reconcile_id), False)
        # check if you can delete
        for spread_line in invoice1.invoice_line.spread_line_ids:
            previous_move = spread_line.move_id.ids
            spread_line.unlink_move()
            # exists?
            self.assertEqual(spread_line.move_id.ids, [])
            self.assertEqual(
                len(self.env['account.move'].search(
                    [('id', 'in', previous_move)])),
                0
            )

        # make account_fx_income_id reconcilable
        self.account_fx_income.write({'reconcile': True})
        # make an invoice with the new reconcilable account
        invoice2 = self.account_invoice_obj.create({
            'account_id': self.account_fx_income.id,
            'company_id': self.partner.company_id.id,
            'currency_id': self.currency_usd.id,
            'invoice_line': [(
                0, 0, {'account_id': self.account_fx_income.id,
                       'name': 'line1',
                       'product_id': self.product.id,
                       'quantity': 2000,
                       'uos_id': self.product.uos_id.id,
                       'price_unit': 33}
            )],
            'journal_id': self.bank_journal_usd.id,
            'partner_id':  self.partner.id,
            'reference_type': 'none'
        })

        # confirm the invoice
        invoice2.action_date_assign()
        invoice2.action_move_create()
        invoice2.action_number()
        invoice2.invoice_validate()
        self.assertEqual(invoice2.date_invoice, fields.Date.today())

        # Make a spread on the line for the next 4 months
        # TODO a period must exist, verify that is always the case
        invoice2.invoice_line[0].write({
            'spread_account_id': self.account_fx_income.id,
            'period_number': 4,
            'period_type': 'month',
            'spread_date': fields.Date.to_string(today.replace(day=1))
        })
        invoice2.invoice_line[0].action_recalculate_spread()
        self.assertEqual(len(invoice2.invoice_line.spread_line_ids), 4)
        moves = []
        for spread in invoice2.invoice_line.spread_line_ids:
            moves += spread.create_move()

        # account cannot be reconciled
        for move in self.env['account.move'].browse(moves):
            for line in move.line_id:
                self.assertEqual(bool(line.reconcile_id), True)
        for spread_line in invoice1.invoice_line.spread_line_ids:
            previous_move = spread_line.move_id.ids
            spread_line.unlink_move()
            self.assertEqual(spread_line.move_id.ids, [])
            self.assertEqual(
                self.env['account.move'].search_count(
                    [('id', 'in', previous_move)]
                ),
                0
            )
