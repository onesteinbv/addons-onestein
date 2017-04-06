# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.exceptions import Warning as UserError
from openerp.tests.common import TransactionCase
from datetime import datetime


class TestVatStatement(TransactionCase):

    def setUp(self):
        super(TestVatStatement, self).setUp()

        self.Statement = self.env['l10n.nl.vat.statement']
        self.StatLine = self.env['l10n.nl.vat.statement.line']
        self.DateRange = self.env['date.range']
        self.DateRangeType = self.env['date.range.type']
        self.Config = self.env['l10n.nl.vat.statement.config']
        self.Tag = self.env['account.account.tag']
        self.Tax = self.env['account.tax']
        self.Invoice = self.env['account.invoice']
        self.InvoiceLine = self.env['account.invoice.line']
        self.Wizard = self.env['l10n.nl.vat.statement.config.wizard']

        self.tag_1 = self.Tag.create({
            'name': 'Tag 1',
            'applicability': 'taxes',
        })

        self.tag_2 = self.Tag.create({
            'name': 'Tag 2',
            'applicability': 'taxes',
        })

        self.tax_1 = self.Tax.create({
            'name': 'Tax 1',
            'amount': 21,
            'tag_ids': [(6, 0, [self.tag_1.id])],
        })

        self.tax_2 = self.Tax.create({
            'name': 'Tax 2',
            'amount': 21,
            'tag_ids': [(6, 0, [self.tag_2.id])],
        })

        self.config = self.Config.create({
            'company_id': self.env.user.company_id.id,
            'tag_1a_omzet': self.tag_1.id,
            'tag_1a_btw': self.tag_2.id,
        })

        self.daterange_type = self.DateRangeType.create({'name': 'Type 1'})

        self.daterange_1 = self.DateRange.create({
            'name': 'Daterange 1',
            'type_id': self.daterange_type.id,
            'date_start': '2016-01-01',
            'date_end': '2016-12-31',
        })

        self.statement_1 = self.Statement.create({
            'name': 'Statement 1',
        })

        self.journal_1 = self.env['account.journal'].create({
            'name': 'Journal 1',
            'code': 'Jou1',
            'type': 'sale',
        })

        self.partner = self.env['res.partner'].create({
            'name': 'Test partner'})

        type_account = self.env.ref('account.data_account_type_receivable')

        invoice_line_account = self.env['account.account'].search([
            ('user_type_id', '=', type_account.id)
        ], limit=1).id

        self.invoice_1 = self.Invoice.create({
            'partner_id': self.partner.id,
            'account_id': invoice_line_account,
            'journal_id': self.journal_1.id,
            'date_invoice': datetime.today(),
            'type': 'out_invoice',
        })

        self.invoice_line_1 = self.InvoiceLine.create({
            'name': 'Test line',
            'quantity': 1.0,
            'account_id': invoice_line_account,
            'price_unit': 100.0,
            'invoice_id': self.invoice_1.id,
            'invoice_line_tax_ids': [(6, 0, [self.tax_1.id])],
        })

        self.invoice_line_2 = self.InvoiceLine.create({
            'name': 'Test line 2',
            'quantity': 1.0,
            'account_id': invoice_line_account,
            'price_unit': 50.0,
            'invoice_id': self.invoice_1.id,
            'invoice_line_tax_ids': [(6, 0, [self.tax_2.id])],
        })

    def test_01_onchange(self):
        self.statement_1.write({'date_range_id': self.daterange_1.id})
        self.statement_1.onchange_date_range_id()
        self.assertEqual(self.statement_1.from_date, '2016-01-01')
        self.assertEqual(self.statement_1.to_date, '2016-12-31')

        self.statement_1.onchange_date()
        check_name = self.statement_1.company_id.name
        check_name += ': ' + ' '.join(
            [self.statement_1.from_date, self.statement_1.to_date])
        self.assertEqual(self.statement_1.name, check_name)

    def test_02_post(self):
        self.statement_1.post()
        self.assertEqual(self.statement_1.state, 'posted')
        self.assertTrue(self.statement_1.date_posted)

    def test_03_reset(self):
        self.statement_1.reset()
        self.assertEqual(self.statement_1.state, 'draft')
        self.assertFalse(self.statement_1.date_posted)

    def test_04_write(self):
        self.statement_1.post()
        with self.assertRaises(UserError):
            self.statement_1.write({'name': 'Test Name'})

    def test_05_unlink_exception(self):
        self.statement_1.post()
        with self.assertRaises(UserError):
            self.statement_1.unlink()

    def test_06_unlink_working(self):
        self.statement_1.unlink()

    def test_07_update_exception1(self):
        self.statement_1.post()
        with self.assertRaises(UserError):
            self.statement_1.update()

    def test_08_update_exception2(self):
        self.config.unlink()
        with self.assertRaises(UserError):
            self.statement_1.update()

    def test_09_update_working(self):
        self.invoice_1._onchange_invoice_line_ids()
        self.invoice_1.signal_workflow('invoice_open')
        self.statement_1.update()
        self.assertEqual(len(self.statement_1.line_ids.ids), 19)

        _1 = self.StatLine.search(
            [('code', '=', '1'), ('id', 'in', self.statement_1.line_ids.ids)],
            limit=1)

        _1a = self.StatLine.search(
            [('code', '=', '1a'), ('id', 'in', self.statement_1.line_ids.ids)],
            limit=1)

        self.assertFalse(_1.format_omzet)
        self.assertFalse(_1.format_btw)
        self.assertTrue(_1.is_group)

        self.assertEqual(_1a.format_omzet, '100.00')
        self.assertEqual(_1a.format_btw, '10.50')
        self.assertFalse(_1a.is_group)

    def test_10_line_unlink_exception(self):
        self.invoice_1.signal_workflow('invoice_open')
        self.statement_1.update()
        self.statement_1.post()
        with self.assertRaises(UserError):
            self.statement_1.line_ids.unlink()

    def test_11_wizard_execute(self):
        wizard = self.Wizard.create({})

        self.assertEqual(wizard.tag_1a_omzet, self.tag_1)
        self.assertEqual(wizard.tag_1a_btw, self.tag_2)

        wizard.write({
            'tag_1a_btw': self.tag_1.id,
            'tag_1a_omzet': self.tag_2.id,
        })

        self.config.unlink()

        wizard_2 = self.Wizard.create({})
        self.assertNotEqual(wizard_2.tag_1a_omzet, self.tag_1)
        self.assertNotEqual(wizard_2.tag_1a_btw, self.tag_2)

        config = self.Config.search(
            [('company_id', '=', self.env.user.company_id.id)],
            limit=1)
        self.assertFalse(config)

        wizard.execute()

        config = self.Config.search(
            [('company_id', '=', self.env.user.company_id.id)],
            limit=1)
        self.assertTrue(config)
        self.assertEqual(config.tag_1a_btw, self.tag_1)
        self.assertEqual(config.tag_1a_omzet, self.tag_2)
