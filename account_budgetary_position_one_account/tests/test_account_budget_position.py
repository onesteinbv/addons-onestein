# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestAccountBudgetPosition(common.TransactionCase):

    def setUp(self):
        super(TestAccountBudgetPosition, self).setUp()

        self.Post = self.env['account.budget.post']
        self.Account = self.env['account.account']

        self.receivable = self.env.ref('account.data_account_type_receivable')
        self.payable = self.env.ref('account.data_account_type_payable')

        self.account_1 = self.Account.search([
            ('user_type_id', '=', self.receivable.id)
        ], limit=1).id

        self.account_2 = self.Account.search([
            ('user_type_id', '=', self.payable.id)
        ], limit=1).id

        self.post_1 = self.Post.create({
            'name': 'Post 1',
            'account_ids': [(6, 0, [self.account_1, self.account_2])]
        })

        self.post_2 = self.Post.create({
            'name': 'Post 2',
        })

        self.post_3 = self.Post.create({
            'name': 'Post 3',
            'account_id': self.account_1
        })

    def test_01_create(self):
        self.assertEqual(self.post_3.account_ids.ids, [self.account_1])

    def test_02_get_account_id(self):
        self.assertEqual(self.post_1.account_id.id, self.account_1)
        self.assertFalse(self.post_2.account_id)

    def test_03_set_account_id(self):
        self.post_1.write({'account_id': None})
        self.assertFalse(self.post_1.account_ids)

        self.post_2.write({'account_id': self.account_2})
        self.assertEqual(self.post_2.account_ids.ids, [self.account_2])
