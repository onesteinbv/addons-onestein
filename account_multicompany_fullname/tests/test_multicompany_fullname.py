# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMulticompanyFullname(TransactionCase):

    def setUp(self):
        super(TestMulticompanyFullname, self).setUp()
        self.fp = self.env['account.fiscal.position'].create({
            'name': 'FP 1',
            'company_id': self.env.user.company_id.id,
        })

    def test_01_name_get(self):
        self.assertEqual(
            self.fp.name_get()[0][1],
            'FP 1 - %s' % self.env.user.company_id.name)
