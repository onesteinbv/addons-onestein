# -*- coding: utf-8 -*-
# License AGPL-3.0 or later [http://www.gnu.org/licenses/agpl].

from openerp.tests.common import TransactionCase
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import date


class TestAccountCostSpread(TransactionCase):

    def setUp(self):
        super(TestAccountCostSpread, self).setUp()
        self.acc_inv_model = self.env['account.invoice']
        self.acc_inv_l_model = self.env['account.invoice.line']
        self.acc_inv_spread_l_model = self.env['account.invoice.spread.line']
        self.res_currency_model = self.env['res.currency']
        self.partner_agrolait_id = self.env.ref(
            "base.res_partner_2"
        )
        self.currency_usd_id = self.env.ref("base.USD")
        self.account_fx_income_id = self.env.ref("account.income_fx_income")
        self.account_fx_expense_id = self.ref("account.income_fx_expense")
        self.product_id = self.ref("product.product_product_4")
        self.bank_journal_usd_id = self.env.ref("account.bank_journal_usd")
        self.account_usd_id = self.env.ref("account.usd_bnk")


    def test_all(self):
        # make product with account
        self.product_t = self.env['product.product'].create({
            'name': 'product_demo',
            'type': 'service',
            'uos_id': self.env.ref('product.product_uom_categ_unit').id,
        })
        self.invoice = self.acc_inv_model.create({
            'account_id': self.account_fx_income_id.id,
            'company_id': self.partner_agrolait_id.company_id.id,
            'currency_id': self.currency_usd_id.id,
            'invoice_line': [(
                0, 0, {'account_id': self.account_fx_income_id.id,
                       'name': 'line1',
                       'product_id': self.product_t.id,
                       'quantity': 2000,
                       'uos_id': self.product_t.uos_id.id,
                       'price_unit': 33}
            )],
            'journal_id': self.bank_journal_usd_id.id,
            'partner_id':  self.partner_agrolait_id.id,
            'reference_type': 'none'
        })
        # confirm
        self.invoice.action_date_assign()
        self.invoice.action_move_create()
        self.invoice.action_number()
        self.invoice.invoice_validate()
        self.assertEqual(
            self.invoice.date_invoice, date.today().strftime(
                DEFAULT_SERVER_DATE_FORMAT
            )
        )
        # create spread for this now confirmed invoice (if not confirmed it
        # would not have a date,
        # Make a spread on the line for the next 4 months
        # make invoice if the start date is intramonth the first spread  will
        # be proportiaonally less, the others will be equal, if there is some
        # left it will be added to an extra month. So in order to have exactly
        # 4 months we must impose start date to the beginning of the month.
        
        self.invoice.invoice_line[0].write(
            {'spread_account_id': self.account_fx_income_id.id,
             'period_number': 4,
             'period_type': 'month',
             'spread_date': date.today().replace(day=1).strftime(
                 DEFAULT_SERVER_DATE_FORMAT
             )}
        )

        # if the test is launched after september and the spread goes beyond 
        # current year we need to create new fiscalyear this year + 1

        self.next_fiscalyear = self.env['account.fiscalyear'].create({
            'name': 'thisyear',
            'code': 'THS',
            'company_id': 1,
            'date_start': date.today().replace(
                year=date.today().year+1, month=1, day=1).strftime(
                    DEFAULT_SERVER_DATE_FORMAT),
            'date_stop': date.today().replace(
                year=date.today().year+1, month=12, day=31).strftime(
                    DEFAULT_SERVER_DATE_FORMAT)
        })

        # make period IDS for this fy
        result = self.next_fiscalyear.create_period()



        self.invoice.invoice_line[0].action_recalculate_spread()
        self.assertEqual(len(self.invoice.invoice_line.spread_line_ids), 4)
        # create move for every spread
        moves = []
        for spread_l in self.invoice.invoice_line.spread_line_ids:
            moves += spread_l.create_move()
        # account cannot be reconciled
        for move in self.env['account.move'].browse(moves):
            for line in move.line_id:
                self.assertEqual(bool(line.reconcile_id), False)
        # check if you can delete
        for spread_l in self.invoice.invoice_line.spread_line_ids:
            previous_move = spread_l.move_id.ids
            spread_l.unlink_move()
            # exists?
            self.assertEqual(spread_l.move_id.ids, [])
            self.assertEqual(
                len(self.env['account.move'].search(
                    [('id', 'in', previous_move)])),
                0
            )
        # make account_fx_income_id reconcilable
        self.account_fx_income_id.write({'reconcile': True})
        # make an invoice with the new reconciliable account
        self.invoice_rec = self.acc_inv_model.create({
            'account_id': self.account_fx_income_id.id,
            'company_id': self.partner_agrolait_id.company_id.id,
            'currency_id': self.currency_usd_id.id,
            'invoice_line': [(
                0, 0, {'account_id': self.account_fx_income_id.id,
                       'name': 'line1',
                       'product_id': self.product_t.id,
                       'quantity': 2000,
                       'uos_id': self.product_t.uos_id.id,
                       'price_unit': 33}
            )],
            'journal_id': self.bank_journal_usd_id.id,
            'partner_id':  self.partner_agrolait_id.id,
            'reference_type': 'none'
        })
        # confirm
        self.invoice_rec.action_date_assign()
        self.invoice_rec.action_move_create()
        self.invoice_rec.action_number()
        self.invoice_rec.invoice_validate()
        self.assertEqual(
            self.invoice_rec.date_invoice, date.today().strftime(
                DEFAULT_SERVER_DATE_FORMAT
            )
        )
        # Make a spread on the line for the next 4 months
        # TODO a period must exist, verify that is allways the case
        self.invoice_rec.invoice_line[0].write(
            {'spread_account_id': self.account_fx_income_id.id,
             'period_number': 4,
             'period_type': 'month',
             'spread_date': date.today().replace(day=1).strftime(
                 DEFAULT_SERVER_DATE_FORMAT)
            }
        )
        self.invoice_rec.invoice_line[0].action_recalculate_spread()
        self.assertEqual(len(self.invoice_rec.invoice_line.spread_line_ids), 4)
        moves = []
        for spread in self.invoice_rec.invoice_line.spread_line_ids:
            moves += spread.create_move()
        # account cannot be reconciled
        for move in self.env['account.move'].browse(moves):
            for line in move.line_id:
                self.assertEqual(bool(line.reconcile_id), True)
        for spread_l in self.invoice.invoice_line.spread_line_ids:
            previous_move = spread_l.move_id.ids
            spread_l.unlink_move()
            self.assertEqual(spread_l.move_id.ids, [])
            self.assertEqual(
                len(
                    self.env['account.move'].search(
                        [('id', 'in', previous_move)]
                    )
                ),
                0
            )
