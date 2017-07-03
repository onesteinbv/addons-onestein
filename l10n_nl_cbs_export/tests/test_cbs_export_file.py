# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.exceptions import ValidationError


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
        type_account = self.env.ref('account.data_account_type_receivable')
        invoice_line_account = self.env['account.account'].search([
            ('user_type_id', '=', type_account.id)
        ], limit=1)

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
                    'account_id': invoice_line_account.id,
                    'price_unit': 50.0,
                    'product_id': service.id,
                    'quantity': 5.0
                }),
                (0, False, {
                    'name': 'Sale of consumable',
                    'invoice_line_tax_ids': [(6, 0, [tax1.id])],
                    'account_id': invoice_line_account.id,
                    'price_unit': 35.0,
                    'product_id': consumable.id,
                    'quantity': 1.0
                }),
            ]
        })

        # Create a new invoice to partner1, dated this month, price: 450
        a_date_in_this_month = date.today()
        invoice2 = self.env['account.invoice'].create({
            'reference_type': 'none',
            'name': 'invoice to client',
            'account_id': self.account_receivable.id,
            'type': 'out_invoice',
            'fiscal_position_id': fp.id,
            'date_invoice': a_date_in_this_month.strftime(DF),
            'partner_id': partner1.id,
            'invoice_line_ids': [
                (0, False, {
                    'name': 'Sale of service',
                    'invoice_line_tax_ids': [(6, 0, [tax1.id])],
                    'account_id': invoice_line_account.id,
                    'price_unit': 50.0,
                    'product_id': service.id,
                    'quantity': 5.0
                }),
                (0, False, {
                    'name': 'Sale of consumable',
                    'invoice_line_tax_ids': [(6, 0, [tax1.id])],
                    'account_id': invoice_line_account.id,
                    'price_unit': 35.0,
                    'product_id': consumable.id,
                    'quantity': 1.0
                }),
                (0, False, {
                    'name': 'Sale of another consumable',
                    'invoice_line_tax_ids': [(6, 0, [tax1.id])],
                    'account_id': invoice_line_account.id,
                    'price_unit': 120.0,
                    'product_id': consumable.id,
                    'quantity': 2.0
                }),
            ]
        })

        # validate the invoices
        invoice1.action_invoice_open()
        invoice2.action_invoice_open()

    def test_01_defaults(self):

        # Create a default CBS Export File record
        cbs_export = self.env['cbs.export.file'].create({})
        self.assertTrue(cbs_export)
        self.assertEqual(cbs_export.company_id, self.company)

        # Test record year
        this_year = date.today().strftime('%Y')
        self.assertEqual(cbs_export.year, this_year)

        # Test record month
        this_month = date.today().strftime('%m')
        self.assertEqual(cbs_export.month, this_month)

        # Test record name
        cbs_export_name = 'CBS_'
        cbs_export_name += str(this_year)[2:4] + str(this_month)
        self.assertEqual(cbs_export.name[0:8], cbs_export_name)

    def test_02_check_wrong_year(self):

        # Should raise error about wrong year
        with self.assertRaises(ValidationError):
            self.env['cbs.export.file'].create({'year': '201x'})

    def test_03_export_file(self):

        # Create a CBS Export File record
        cbs_export = self.env['cbs.export.file'].create({})
        cbs_export.export_file()
        self.assertTrue(cbs_export.cbs_export_invoice)

        # Test file name
        filename = '%s_%s.csv' % (cbs_export.month, cbs_export.year)
        self.assertEqual(cbs_export.filename, filename)

        # Generate the csv file
        cbs_export.get_data()
        result_file = cbs_export.cbs_export_invoice.decode('base64')
        self.assertTrue(result_file)

        # Check lines length
        for result_line in result_file.splitlines():
            self.assertEqual(len(result_line), 115)

    def test_04_run_cron_job(self):

        last_month = date.today() + relativedelta(months=-1)

        # Verify that the CBS record was not created for the last month
        prev_cbs_export = self.env['cbs.export.file'].search([
            ('month', '=', last_month.strftime("%m")),
            ('year', '=', last_month.strftime("%Y"))
        ])
        self.assertFalse(prev_cbs_export)

        # Run job "Generate CBS Export File"
        self.env['cbs.export.file'].cron_get_cbs_export_file()

        # Verify that the CBS record was generated
        cbs_export1 = self.env['cbs.export.file'].search([
            ('month', '=', last_month.strftime("%m")),
            ('year', '=', last_month.strftime("%Y")),
            ('company_id', '=', self.company.id)
        ])
        self.assertTrue(cbs_export1)
        self.assertEqual(len(cbs_export1), 1)

        # Verify that the csv file was generated
        result_file = cbs_export1.cbs_export_invoice.decode('base64')
        self.assertTrue(result_file)

        # Run again job "Generate CBS Export File"
        self.env['cbs.export.file'].cron_get_cbs_export_file()

        # Verify that no other CBS records are generated
        cbs_export2 = self.env['cbs.export.file'].search([
            ('month', '=', last_month.strftime("%m")),
            ('year', '=', last_month.strftime("%Y")),
            ('company_id', '=', self.company.id)
        ])
        self.assertTrue(cbs_export2)
        self.assertEqual(len(cbs_export2), 1)

    def test_05_no_invoices(self):

        next_month_dt = date.today() + relativedelta(months=1)
        next_month = next_month_dt.strftime("%m")
        next_month_year = next_month_dt.strftime("%Y")

        cbs_export = self.env['cbs.export.file'].create({
            'month': next_month
        })
        self.assertTrue(cbs_export)

        # Verify that there are no invoices for next month
        invoices = self.env['account.invoice'].search([
            ('type', '=', 'out_invoice'),
            ('state', 'in', ['open', 'paid']),
            ('company_id', '=', cbs_export.company_id.id),
            ('date_invoice', '>=', datetime.strptime(
                '%s-%s-%s' % (
                    1, int(next_month), int(next_month_year)
                ), '%d-%m-%Y')
             )]
        )
        self.assertFalse(invoices)

        # Trying to export the CBS file raises an error
        with self.assertRaises(ValidationError):
            cbs_export.get_data()
