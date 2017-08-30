# -*- coding: utf-8 -*-
# License AGPL-3.0 or later [http://www.gnu.org/licenses/agpl].

from openerp.tests.common import TransactionCase
from openerp import fields, tools
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.modules import get_module_resource
from datetime import date


class TestAccountCostSpread(TransactionCase):

    def setUp(self):
        super(TestAccountCostSpread, self).setUp()
        self.acc_inv_model = self.env['account.invoice']
        self.acc_inv_l_model = self.env['account.invoice.line']
        self.acc_inv_spread_l_model = self.env['account.invoice.spread.line']
        self.acc_bank_stmt_model = self.env['account.bank.statement']
        self.acc_bank_stmt_l_model = self.env['account.bank.statement.line']
        self.res_currency_model = self.env['res.currency']
        self.res_currency_rate_model = self.env['res.currency.rate']
        self.partner_agrolait_id = self.env.ref(
            "base.res_partner_2"
        )
        self.currency_swiss_id = self.env.ref("base.CHF")
        self.currency_usd_id = self.env.ref("base.USD")
        self.account_rcv_id = self.env.ref("account.a_recv")
        self.account_fx_income_id = self.env.ref(
                "account.income_fx_income"
        )
        self.account_fx_expense_id = self.ref(
             "account.income_fx_expense"
        )
        self.product_id = self.ref("product.product_product_4")
        self.bank_journal_usd_id = self.env.ref("account.bank_journal_usd")
        self.account_usd_id = self.env.ref("account.usd_bnk")
        # make product with account
        self.product_t = self.env['product.product'].create({
            'name':  'product_demo',
            'type': 'service',
            'uos_id': self.env.ref('product.product_uom_categ_unit').id,
        })
        # make invoice
        self.invoice = self.acc_inv_model.create({
            'account_id': self.account_fx_income_id.id,
            'company_id': self.partner_agrolait_id.company_id.id,
            'currency_id': self.currency_usd_id.id,
            'invoice_line': [(
                0, 0, {'account_id': self.account_fx_income_id.id,
                       'name': 'line1' ,
                       'product_id': self.product_t.id,
                       'product_uom_qty': 2000,
                       'uos_id': self.product_t.uos_id.id,
                       'price_unit': 33}
            )],
            'journal_id': self.bank_journal_usd_id.id ,
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
        # would not have a date, therefore gen error

        #Make a spread on the line for the next 4 months
        self.invoice.invoice_line[0].write(
            {'spread_account_id': self.account_fx_income_id.id,
             'period_number': 4,
             'period_type': 'month',
            }
        )
        self.invoice.invoice_line[0].action_recalculate_spread()
        self.assertEqual(len(self.invoice.invoice_line.spread_line_ids), 4)
        # create move for every spread
        moves=[]
        for spread in self.invoice.invoice_line.spread_line_ids:
            moves += spread.create_move()
        #check if reconciled
        for move in moves:
            self.assertEqual(bool(move.line_id.reconcile_id), True)
        #check if you can delete
