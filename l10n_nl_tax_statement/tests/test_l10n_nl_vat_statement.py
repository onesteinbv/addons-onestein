# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import Warning as UserError
from odoo.tests.common import TransactionCase


class TestVatStatement(TransactionCase):

    def setUp(self):
        super(TestVatStatement, self).setUp()

        self.Statement = self.env['l10n.nl.vat.statement']
        self.DateRange = self.env['date.range']
        self.DateRangeType = self.env['date.range.type']
        self.Config = self.env['l10n.nl.vat.statement.config']

        self.config = self.Config.create(
            {'company_id': self.env.user.company_id.id})

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

    def test_05_unlink(self):
        self.statement_1.post()
        with self.assertRaises(UserError):
            self.statement_1.unlink()

    def test_06_update_exception(self):
        self.statement_1.post()
        with self.assertRaises(UserError):
            self.statement_1.update()

    def test_07_update_working(self):
        self.statement_1.update()
        self.assertEqual(len(self.statement_1.line_ids.ids), 19)
