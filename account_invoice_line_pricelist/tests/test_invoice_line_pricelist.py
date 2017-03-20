# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from odoo.tests.common import TransactionCase


class TestInvoiceLinePricelist(TransactionCase):

    def setUp(self):
        super(TestInvoiceLinePricelist, self).setUp()

        self.eur = self.env.ref('base.EUR')
        self.usd = self.env.ref('base.USD')

        self.journal_1 = self.env['account.journal'].create({
            'name': 'Journal 1',
            'code': 'Jou1',
            'type': 'sale',
        })

        self.journal_2 = self.env['account.journal'].create({
            'name': 'Journal 2',
            'code': 'Jou2',
            'type': 'purchase',
        })

        self.template = self.env['product.template'].create({
            'name': 'Test Product',
            'lst_price': 10.00,
            'sale_line_warn': 'no-message',
        })

        self.product = self.template.product_variant_id

        self.plist1 = self.env['product.pricelist'].create({
            'name': 'Test pricelist 1',
            'currency_id': self.usd.id,
            'item_ids': [
                (0, 0, {
                    'name': 'Test item default',
                    'base': 'list_price',
                    'applied_on': '3_global',
                    'percent_price': -10,
                    'compute_price': 'percentage',
                })],
        })
        self.plist2 = self.env['product.pricelist'].create({
            'name': 'Test pricelist 2',
            'currency_id': self.usd.id,
            'item_ids': [
                (0, 0, {
                    'name': 'Test item default',
                    'base': 'list_price',
                    'applied_on': '3_global',
                    'percent_price': -20,
                    'compute_price': 'percentage',
                })],
        })
        self.partner = self.env['res.partner'].create(
            {'name': 'Test partner',
             'property_product_pricelist': self.plist1.id})
        type_account = self.env.ref('account.data_account_type_receivable')
        invoice_line_account = self.env['account.account'].search([
            ('user_type_id', '=', type_account.id)
        ], limit=1).id

        self.invoice_1 = self.env['account.invoice'].create(
            {
                'partner_id': self.partner.id,
                'account_id': invoice_line_account,
                'currency_id': self.usd.id,
                'journal_id': self.journal_1.id,
                'pricelist_id': self.plist1.id,
                'date_invoice': datetime.today(),
                'type': 'out_invoice',
            }
        )

        self.invoice_2 = self.env['account.invoice'].create(
            {
                'partner_id': self.partner.id,
                'account_id': invoice_line_account,
                'currency_id': self.usd.id,
                'journal_id': self.journal_2.id,
                'pricelist_id': self.plist1.id,
                'date_invoice': datetime.today(),
                'type': 'in_invoice',
            }
        )

        self.invoice_line = self.env['account.invoice.line'].create(
            {'name': 'Test line',
             'quantity': 1.0,
             'account_id': invoice_line_account,
             'price_unit': 1.0,
             'invoice_id': self.invoice_1.id})

        self.invoice_line_2 = self.env['account.invoice.line'].create(
            {'name': 'Test line 2',
             'quantity': 1.0,
             'account_id': invoice_line_account,
             'price_unit': 1.0,
             'invoice_id': self.invoice_2.id})

    def test_01_onchange_product_id_pricelist(self):
        exp_value = 11.0
        self.invoice_line.write({
            'product_id': self.product.id,
            'uom_id': self.product.uom_id.id,
            'quantity': 1.0,
            'partner_id': self.partner.id,
            'company_id': self.env.user.company_id.id
        })
        self.invoice_line._onchange_product_id()
        self.assertLessEqual(
            abs(exp_value - self.invoice_line.price_unit), 0.0001,
            "ERROR in getting price from pricelist")

    def test_02_onchange_product_id_invoice_pricelist(self):
        exp_value = 12.0
        self.invoice_line.write({
            'product_id': self.product.id,
            'uom_id': self.product.uom_id.id,
            'quantity': 1.0,
            'partner_id': self.partner.id,
            'company_id': self.env.user.company_id.id
        })
        self.invoice_1.write({'pricelist_id': self.plist2.id})
        self.invoice_line._onchange_product_id()
        self.assertLessEqual(
            abs(exp_value - self.invoice_line.price_unit), 0.0001,
            "ERROR in getting price from pricelist")

    def test_03_onchange_product_id_different_currency(self):
        currency = self.usd
        exp_value = currency.round((11.00 / currency.rate))
        self.invoice_line.write({
            'product_id': self.product.id,
            'uom_id': self.product.uom_id.id,
            'quantity': 1.0,
            'partner_id': self.partner.id,
            'company_id': self.env.user.company_id.id
        })
        self.plist1.write({'currency_id': self.eur.id})
        self.invoice_line._onchange_product_id()
        self.assertLessEqual(
            abs(exp_value - self.invoice_line.price_unit), 0.0001,
            "ERROR in getting price from pricelist")

    def test_04_ignore(self):
        self.invoice_1.write({'pricelist_id': None})
        self.invoice_line.write({
            'product_id': self.product.id,
            'uom_id': self.product.uom_id.id,
            'quantity': 1.0,
            'partner_id': self.partner.id,
            'company_id': self.env.user.company_id.id
        })
        self.invoice_line._onchange_product_id()
        self.assertLessEqual(self.invoice_line.price_unit, 10.0,
                             "ERROR in getting price from pricelist")

        self.invoice_line_2.write({
            'product_id': self.product.id,
            'uom_id': self.product.uom_id.id,
            'quantity': 1.0,
            'partner_id': self.partner.id,
            'company_id': self.env.user.company_id.id
        })
        self.invoice_line_2._onchange_product_id()
        self.assertLessEqual(self.invoice_line_2.price_unit, 1.0,
                             "ERROR in getting price from pricelist")
