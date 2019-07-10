# -*- coding: utf-8 -*-
# License AGPL-3.0 or later [http://www.gnu.org/licenses/agpl].

from openerp import fields
from openerp.tests.common import TransactionCase


class TestAccountCostSpread(TransactionCase):
    # pylint: disable=too-many-instance-attributes

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
        self.company = self.partner.company_id
        self.currency = self.env.ref('base.main_company').currency_id
        self.account_fx_income = self.env.ref("account.income_fx_income")
        self.account_fx_expense = self.ref("account.income_fx_expense")
        self.bank_journal_usd = self.env.ref("account.bank_journal_usd")
        self.product = self.env['product.product'].create({
            'name': 'product_demo',
            'type': 'service',
            'uos_id': self.env.ref('product.product_uom_categ_unit').id,
        })

        # Some of our test spreads go beyond current year.
        # So we need to create a new fiscalyear, this year + 1.
        self.today_string = fields.Date.context_today(self.product)
        self.today = fields.Date.from_string(self.today_string)
        self.next_fiscalyear = self.env['account.fiscalyear'].create({
            'name': 'thisyear',
            'code': 'THS',
            'company_id': self.company.id,
            'date_start': fields.Date.to_string(
                self.today.replace(year=self.today.year+1, month=1, day=1)),
            'date_stop': fields.Date.to_string(
                self.today.replace(year=self.today.year+1, month=12, day=31))
        })
        self.next_fiscalyear.create_period()

        # create invoice with test product and account
        self.invoice1 = self.account_invoice_obj.create({
            'account_id': self.account_fx_income.id,
            'company_id': self.partner.company_id.id,
            'currency_id': self.currency.id,
            'invoice_line': [(0, 0, {
                'account_id': self.account_fx_income.id,
                'name': 'line1',
                'product_id': self.product.id,
                'quantity': 400,
                'uos_id': self.product.uos_id.id,
                'price_unit': 33
            })],
            'journal_id': self.bank_journal_usd.id,
            'partner_id':  self.partner.id,
            'reference_type': 'none'
        })

    def test_4_months(self):
        """ Test cost spreading """
        self.assertFalse(self.invoice1.date_invoice)
        self.assertTrue(self.invoice1.invoice_line.spread_date_required)

        # confirm invoice
        self.invoice1.action_date_assign()
        self.invoice1.action_move_create()
        self.invoice1.action_number()
        self.invoice1.invoice_validate()
        self.assertEqual(self.invoice1.date_invoice, self.today_string)
        self.assertFalse(self.invoice1.invoice_line.spread_date_required)

        # Make a spread on the line for the first 4 months of the year.
        self.invoice1.invoice_line[0].write({
            'spread_account_id': self.account_fx_income.id,
            'period_number': 4,
            'period_type': 'month',
            'spread_date': fields.Date.to_string(
                self.today.replace(day=1, month=1)
            )
        })
        self.invoice1.invoice_line[0].action_recalculate_spread()

        # This is an exact spread, so from first of month to end of a month.
        # So it should have 4 equal periods of 3300 euros each.
        spread_lines = self.invoice1.invoice_line.spread_line_ids
        amounts = spread_lines.mapped('amount')
        self.assertEqual(len(spread_lines), 4)
        self.assertEqual(min(amounts), 3300.0)
        self.assertEqual(max(amounts), 3300.0)

        # create move for every spread
        moves = []
        for spread_line in self.invoice1.invoice_line.spread_line_ids:
            moves += spread_line.create_move()
        # account cannot be reconciled
        for move in self.env['account.move'].browse(moves):
            for line in move.line_id:
                self.assertEqual(bool(line.reconcile_id), False)
        # check if you can delete
        for spread_line in self.invoice1.invoice_line.spread_line_ids:
            previous_move = spread_line.move_id.ids
            spread_line.unlink_move()
            # exists?
            self.assertEqual(spread_line.move_id.ids, [])
            self.assertEqual(
                len(self.env['account.move'].search(
                    [('id', 'in', previous_move)])),
                0
            )

    def test_16_months(self):
        # confirm invoice
        self.invoice1.action_date_assign()
        self.invoice1.action_move_create()
        self.invoice1.action_number()
        self.invoice1.invoice_validate()

        # Make a spread on the line for the 16 months from Jan 1st.
        self.invoice1.invoice_line[0].write({
            'spread_account_id': self.account_fx_income.id,
            'period_number': 16,
            'period_type': 'month',
            'spread_date': fields.Date.to_string(
                self.today.replace(day=1, month=1))
        })
        self.invoice1.invoice_line[0].action_recalculate_spread()
        spread_lines = self.invoice1.invoice_line.spread_line_ids
        amounts = spread_lines.mapped('amount')
        self.assertEqual(len(spread_lines), 16)
        self.assertEqual(sum(amounts), 3300.0 * 4.0)

    def test_reconcile(self):
        # make account_fx_income_id reconcilable
        self.account_fx_income.write({'reconcile': True})
        # make an invoice with the new reconcilable account
        invoice2 = self.account_invoice_obj.create({
            'account_id': self.account_fx_income.id,
            'company_id': self.partner.company_id.id,
            'currency_id': self.currency.id,
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
        # confirm the invoice
        invoice2.action_date_assign()
        invoice2.action_move_create()
        invoice2.action_number()
        invoice2.invoice_validate()
        self.assertEqual(invoice2.date_invoice, self.today_string)

        # Make a spread on the line for the next 4 months
        # TODO a period must exist, verify that is always the case
        invoice2.invoice_line[0].write({
            'spread_account_id': self.account_fx_income.id,
            'period_number': 4,
            'period_type': 'month',
            'spread_date': fields.Date.to_string(
                self.today.replace(day=1))
        })
        invoice2.invoice_line[0].action_recalculate_spread()
        self.assertEqual(len(invoice2.invoice_line.spread_line_ids), 4)
        moves = []
        for spread in invoice2.invoice_line.spread_line_ids:
            moves += spread.create_move()

        for move in self.env['account.move'].browse(moves):
            # one line must be reconciled
            self.assertEqual(
                len(move.mapped('line_id.reconcile_partial_id')),
                1
            )
        for spread_line in self.invoice1.invoice_line.spread_line_ids:
            previous_move = spread_line.move_id.ids
            spread_line.unlink_move()
            self.assertEqual(spread_line.move_id.ids, [])
            self.assertEqual(
                self.env['account.move'].search_count(
                    [('id', 'in', previous_move)]
                ),
                0
            )
