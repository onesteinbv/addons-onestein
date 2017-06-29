# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.exceptions import UserError


class TestCbsExportFile(TransactionCase):

    def setUp(self):
        super(TestCbsExportFile, self).setUp()

        self.company = self.env.ref('base.main_company')
        company = self.company
        company.country_id = self.env.ref('base.nl')

        type_receivable = self.env.ref('account.data_account_type_receivable')
        self.account_receivable = self.env['account.account'].search(
            [('user_type_id', '=', type_receivable.id)],
            limit=1
        )
        self.land_account = self.env.ref('account.demo_sale_of_land_account')

        Tax = self.env['account.tax']

        # Create a regular fixed tax
        tax1 = Tax.create({
            'name': "Fixed tax",
            'amount_type': 'fixed',
            'amount': 10,
            'sequence': 1,
        })

        # Create a EU partner
        partner1 = self.env['res.partner'].create({
            'name': 'Partner1',
            'is_company': True,
            'street': 'Via Roma, 10',
            'phone': '123456789',
            'email': 'info@partner1.com',
            'type': 'contact',
            'country_id': self.env.ref('base.it').id
        })

        # Get Products
        # On site Monitoring, a service
        service = self.env.ref('product.product_product_1')
        # Optical mouse, a consumable
        consumable = self.env.ref('product.product_product_10')

        # Create a new invoice to partner1, dated last month, price: 250
        a_date_in_last_month = date.today() + \
            relativedelta(day=1, months=-1)
        fp = self.env['account.fiscal.position'].create(
            dict(name="fiscal position", sequence=1)
        )
        invoice1 = self.env['account.invoice'].create({
            'reference_type': 'none',
            'name': 'invoice to client',
            'account_id': self.account_receivable.id,
            'type': 'out_invoice',
            'fiscal_position_id': fp.id,
            'date_invoice': a_date_in_last_month.strftime(DF),
            'partner_id': partner1.id,
            'invoice_line_ids': [
                (0, False, {
                    'name': 'Sale of service',
                    'invoice_line_tax_ids': [(6, 0, [tax1.id])],
                    'account_id': self.land_account.id,
                    'price_unit': 50.0,
                    'product_id': service.id,
                    'quantity': 5.0,
                    'uos_id': self.env.ref('product.product_uom_unit').id
                }),
                (0, False, {
                    'name': 'Sale of consumable',
                    'invoice_line_tax_ids': [(6, 0, [tax1.id])],
                    'account_id': self.land_account.id,
                    'price_unit': 35.0,
                    'product_id': consumable.id,
                    'quantity': 1.0,
                    'uos_id': self.env.ref('product.product_uom_unit').id
                }),
                (0, False, {
                    'name': 'Sale to be excluded from intrastat report',
                    'invoice_line_tax_ids': [(6, 0, [tax1.id])],
                    'account_id': self.land_account.id,
                    'price_unit': 20.0,
                    'product_id': service.id,
                    'quantity': 2.0,
                    'uos_id': self.env.ref('product.product_uom_unit').id
                }),
            ]
        })

        # validate the invoice
        invoice1.action_invoice_open()

    def test_01_defaults(self):

        cbs_export = self.env['cbs.export.file'].create({})
        self.assertTrue(cbs_export)
        self.assertEqual(cbs_export.company_id, self.company)

        context_today = fields.Date.context_today(self)
        this_year = fields.Date.from_string(context_today).strftime('%Y')
        self.assertEqual(cbs_export.year, this_year)

        this_month = fields.Date.from_string(context_today).strftime('%m')
        self.assertEqual(cbs_export.month, this_month)

        cbs_export_name = 'CBS_' + str(this_year)[0:2] + str(this_month) + '1'
        self.assertEqual(cbs_export.name, cbs_export_name)

    def test_02_export_file(self):

        cbs_export = self.env['cbs.export.file'].create({})
        cbs_export.export_file()
        self.assertTrue(cbs_export.cbs_export_invoice)

        filename = '%s_%s.csv' % (cbs_export.month, cbs_export.year)
        self.assertEqual(cbs_export.filename, filename)
