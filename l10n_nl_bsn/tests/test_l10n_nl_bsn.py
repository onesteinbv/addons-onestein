# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestBsn(TransactionCase):

    def setUp(self):
        super(TestBsn, self).setUp()

        self.partner_bsn = self.env['res.partner'].create({
            'name': 'Partner with BSN',
        })

    def test_01_bsn_not_valid(self):
        self.partner_bsn.bsn_number = '123'
        res = self.partner_bsn.onchange_bsn_number()
        self.assertEqual(self.partner_bsn.bsn_number, '0000.00.123')
        warning = res.get('warning')
        self.assertTrue(warning)
        message = warning.get('message')
        self.assertTrue(message)
        msg_txt = 'The BSN you entered (0000.00.123) is not valid.'
        self.assertEqual(message, msg_txt)
        title = warning.get('title')
        self.assertTrue(title)
        self.assertEqual(title, 'Warning!')

    def test_02_bsn_valid(self):
        self.partner_bsn.bsn_number = '100000009'
        res = self.partner_bsn.onchange_bsn_number()
        self.assertEqual(self.partner_bsn.bsn_number, '1000.00.009')
        warning = res.get('warning')
        self.assertFalse(warning)

    def test_03_bsn_another_partner(self):
        new_partner_bsn = self.env['res.partner'].create({
            'name': 'Partner with BSN',
            'bsn_number': '1000.00.009'
        })
        warning = new_partner_bsn._warn_bsn_existing()
        message = warning.get('message')
        self.assertTrue(message)
        msg_txt = 'Another person (Partner with BSN) ' \
                  'has the same BSN (1000.00.009).'
        self.assertEqual(message, msg_txt)
        title = warning.get('title')
        self.assertTrue(title)
        self.assertEqual(title, 'Warning!')
