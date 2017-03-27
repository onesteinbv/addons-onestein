# -*- coding: utf-8 -*-

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.exceptions import Warning as UserError


class TestIntrastatNL(TransactionCase):
    """Tests for this module"""

    def setUp(self):
        super(TestIntrastatNL, self).setUp()

        self.company = self.env.ref('base.main_company')
        self.company.currency_id = self.env.ref('base.EUR')

        type_receivable = self.env.ref('account.data_account_type_receivable')
        self.account_receivable = self.env['account.account'].search(
            [('user_type_id', '=', type_receivable.id)],
            limit=1
        )
        self.land_account = self.env.ref('account.demo_sale_of_land_account')

    def test_date_range(self):
        company = self.company

        # Create a date range type
        type = self.env['date.range.type'].create({
            'name': 'Test date range type',
            'company_id': company.id,
            'allow_overlap': False
        })

        # Create a date range spanning the last three months
        start_date = date.today() + relativedelta(months=-3)
        date_range = self.env['date.range'].create({
            'name': 'FS2016',
            'date_start': start_date.strftime(DF),
            'date_end': fields.Date.today(),
            'company_id': company.id,
            'type_id': type.id
        })

        # Create an empty, draft intrastat report
        report = self.env['l10n_nl.report.intrastat'].create({
            'company_id': company.id,
            'date_from': fields.Date.today(),
            'date_to': fields.Date.today(),
        })

        # test that dates are updated
        report.write({'date_range_id': date_range.id})
        report.onchange_date_range_id()
        self.assertEquals(report.date_from, start_date.strftime(DF))
        self.assertEquals(report.date_to, fields.Date.today())

    def test_generate_report(self):
        # Set our company's country to NL
        Tax = self.env['account.tax']
        company = self.company
        company.country_id = self.env.ref('base.nl')

        # Create an empty, draft intrastat report for this period
        start_date = date.today() + relativedelta(months=-3)
        report = self.env['l10n_nl.report.intrastat'].create({
            'company_id': company.id,
            'date_from': start_date.strftime(DF),
            'date_to': fields.Date.today(),
        })
        self.assertEquals(report.state, 'draft')

        # Generate lines and store initial total
        report.generate_lines()
        total = report.total_amount

        # Create a regular fixed tax
        tax1 = Tax.create({
            'name': "Fixed tax",
            'amount_type': 'fixed',
            'amount': 10,
            'sequence': 1,
        })
        # Create another fixed tax that, when added to an invoice line,
        # removes the line from the intrastat calculation.
        tax2 = Tax.create({
            'name': "Fixed tax 2",
            'amount_type': 'fixed',
            'amount': 10,
            'sequence': 1,
            'exclude_from_intrastat_if_present': True,
        })

        # Create a new partner GhostStep
        # Country is omitted initially
        ghoststep = self.env['res.partner'].create({
            'name': 'GhostStep',
            'is_company': True,
            'street': 'Main Street, 10',
            'phone': '123456789',
            'email': 'info@ghoststep.com',
            'vat': 'FR32123456789',
            'type': 'contact'
        })

        # Get Products
        # On site Monitoring, a service
        service = self.env.ref('product.product_product_1')
        # Optical mouse, a consumable
        consumable = self.env.ref('product.product_product_10')

        # Create a new invoice to GhostStep, dated last month, price: 250
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
            'partner_id': ghoststep.id,
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
                    'invoice_line_tax_ids': [(6, 0, [tax2.id])],
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

        # generate lines again
        report.set_draft()
        report.generate_lines()

        # try to delete the report, must be denied since it's validated
        with self.assertRaises(UserError):
            report.unlink()

        # The invoice should not be included because it has no country,
        # and so is assumed to have the same country as the main company
        self.assertEquals(report.total_amount, total)

        # Now the report is updated with Ghoststep being in France
        ghoststep.write({'country_id': self.env.ref('base.fr').id})
        report.set_draft()
        report.generate_lines()

        # Test if the total amount has increased by the invoice value
        self.assertEquals(report.total_amount - total, 285.0)

        # Test that the reported totals for 'GhostStep' match
        line = report.line_ids.search([('partner_id', '=', ghoststep.id)])
        self.assertEquals(line.amount_service, 250.0)
        self.assertEquals(line.amount_product, 35.0)

        # Create a new invoice to GhostStep, dated last month, in swiss francs
        invoice2 = self.env['account.invoice'].create({
            'reference_type': 'none',
            'name': 'foreign currency invoice to client',
            'currency_id': self.env.ref('base.CHF').id,
            'account_id': self.account_receivable.id,
            'type': 'out_invoice',
            'fiscal_position_id': fp.id,
            'date_invoice': a_date_in_last_month.strftime(DF),
            'partner_id': ghoststep.id,
            'invoice_line_ids': [
                (0, False, {
                    'name': 'Sale of service',
                    'invoice_line_tax_ids': [(6, 0, [tax1.id])],
                    'account_id': self.land_account.id,
                    'price_unit': 100.0,
                    'product_id': service.id,
                    'quantity': 1.0,
                    'uos_id': self.env.ref('product.product_uom_unit').id
                }),
            ]
        })

        # validate the invoice
        invoice2.action_invoice_open()

        # And update the report
        report.set_draft()
        report.generate_lines()

        # Test if the total amount has increased by the invoice value
        # New total should be 285.0 + round(100.00 / 1.3086, 2) = 361.42
        self.assertTrue(abs(report.total_amount - total - 361.42) <= 0.01)

        # try to delete the report, must be denied since it's validated
        with self.assertRaises(UserError):
            report.unlink()

        # set the report to draft and delete it
        report.set_draft()
        report.unlink()
