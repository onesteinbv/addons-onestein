# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.exceptions import UserError


class TestAnalyticAccountState(common.TransactionCase):

    def setUp(self):
        super(TestAnalyticAccountState, self).setUp()

        AnalyticAccount = self.env['account.analytic.account']
        Wizard = self.env['account.analytic.account.approve']

        self.aa_1 = AnalyticAccount.create({
            'name': 'Analytic Account 1',
            'expected_hours': 10.0,
            'expected_turnover': 1000.0,
            'expected_costs': 500.0,
        })

        self.wizard = Wizard.create({})

    def test_01_submit(self):
        self.aa_1.action_submit()
        self.assertEqual(self.aa_1.analytic_state, 'waiting')

    def test_02_expire(self):
        self.aa_1.action_expire()
        self.assertEqual(self.aa_1.analytic_state, 'expired')

    def test_03_cancel(self):
        self.aa_1.action_cancel()
        self.assertEqual(self.aa_1.analytic_state, 'cancel')

    def test_04_approve(self):
        self.aa_1.action_submit()
        self.aa_1.action_approve()
        self.assertEqual(self.aa_1.analytic_state, 'approved')

        self.aa_1.action_cancel()
        with self.assertRaises(UserError):
            self.aa_1.action_approve()

    def test_05_decline(self):
        self.aa_1.action_decline()
        self.assertEqual(self.aa_1.analytic_state, 'declined')

    def test_06_resubmit(self):
        self.aa_1.action_resubmit()
        self.assertEqual(self.aa_1.analytic_state, 'waiting')

    def test_07_reset_to_draft(self):
        self.aa_1.action_reset_to_draft()
        self.assertEqual(self.aa_1.analytic_state, 'draft')

    def test_08_wizard_approve(self):
        self.aa_1.action_submit()
        self.wizard.with_context(
            active_ids=[self.aa_1.id]).approve_analytic_accounts()
        self.assertEqual(self.aa_1.analytic_state, 'approved')
