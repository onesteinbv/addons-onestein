# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestActivityBasedCosting(common.TransactionCase):

    def setUp(self):
        super(TestActivityBasedCosting, self).setUp()

        aa_obj = self.env['account.analytic.account']
        aal_obj = self.env['account.analytic.line']
        proj_obj = self.env['project.project']

        self.aa_1 = aa_obj.create({
            'name': 'Analytic Account 1',
            'expected_hours': 10.0,
            'expected_turnover': 1000.0,
            'expected_costs': 500.0,
        })
        self.aa_2 = aa_obj.create({
            'name': 'Analytic Account 2',
            'expected_hours': 5.0,
            'expected_turnover': 0,
            'expected_costs': 500.0,
        })
        self.aa_3 = aa_obj.create({
            'name': 'Analytic Account 3',
            'expected_hours': 3.0,
            'expected_turnover': 1000,
            'expected_costs': 1000.0,
        })

        self.proj_1 = proj_obj.create({
            'name': 'Project 1',
            'analytic_account_id': self.aa_1.id,
        })
        self.proj_2 = proj_obj.create({
            'name': 'Project 2',
            'analytic_account_id': self.aa_2.id,
        })
        self.proj_3 = proj_obj.create({
            'name': 'Project 3',
            'analytic_account_id': self.aa_3.id,
        })

        self.aa_line_1_1 = aal_obj.create({
            'name': 'AA Line 1,1',
            'unit_amount': 4.0,
            'amount': 1000.0,
            'account_id': self.aa_1.id,
            'project_id': self.proj_1.id,
        })
        self.aa_line_1_2 = aal_obj.create({
            'name': 'AA Line 1,2',
            'unit_amount': 1.0,
            'amount': -500.0,
            'account_id': self.aa_1.id,
            'project_id': self.proj_1.id,
        })
        self.aa_line_2_1 = aal_obj.create({
            'name': 'AA Line 2,1',
            'unit_amount': 6.0,
            'amount': 1000.0,
            'account_id': self.aa_2.id,
            'project_id': self.proj_2.id,
        })
        self.aa_line_2_2 = aal_obj.create({
            'name': 'AA Line 2,2',
            'unit_amount': 4.0,
            'amount': -2000.0,
            'account_id': self.aa_2.id,
            'project_id': self.proj_2.id,
        })
        self.aa_line_3_1 = aal_obj.create({
            'name': 'AA Line 3,1',
            'unit_amount': 1.0,
            'amount': -1000.0,
            'account_id': self.aa_3.id,
            'project_id': self.proj_3.id,
        })
        self.aa_line_3_2 = aal_obj.create({
            'name': 'AA Line 2,2',
            'unit_amount': 2.0,
            'amount': -2000.0,
            'account_id': self.aa_3.id,
            'project_id': self.proj_3.id,
        })

    def test_01_get_hours_left(self):
        self.assertEqual(self.aa_1.hours_left, 5.0)
        self.assertEqual(self.aa_2.hours_left, -5.0)
        self.assertEqual(self.aa_3.hours_left, 0.0)

    def test_02_get_expected_contribution(self):
        self.assertEqual(self.aa_1.expected_contribution, 500.0)
        self.assertEqual(self.aa_1.expected_contribution_perc, 50.0)

        self.assertEqual(self.aa_2.expected_contribution, -500.0)
        self.assertEqual(self.aa_2.expected_contribution_perc, 0.0)

        self.assertEqual(self.aa_3.expected_contribution, 0.0)
        self.assertEqual(self.aa_3.expected_contribution_perc, 0.0)

    def test_03_get_realized_data(self):
        self.assertEqual(self.aa_1.realized_turnover, 1000.0)
        self.assertEqual(self.aa_1.realized_costs, 500.0)
        self.assertEqual(self.aa_1.contribution, 500.0)
        self.assertEqual(self.aa_1.contribution_perc, 50.0)

        self.assertEqual(self.aa_2.realized_turnover, 1000.0)
        self.assertEqual(self.aa_2.realized_costs, 2000.0)
        self.assertEqual(self.aa_2.contribution, -1000.0)
        self.assertEqual(self.aa_2.contribution_perc, -100.0)

        self.assertEqual(self.aa_3.realized_turnover, 0.0)
        self.assertEqual(self.aa_3.realized_costs, 3000.0)
        self.assertEqual(self.aa_3.contribution, -3000.0)
        self.assertEqual(self.aa_3.contribution_perc, 0.0)

    def test_04_get_budget_result(self):
        self.assertEqual(self.aa_1.budget_result_turnover, 0.0)
        self.assertEqual(self.aa_1.budget_result_cost, 0.0)
        self.assertEqual(self.aa_1.budget_result_contribution, 0.0)
        self.assertEqual(self.aa_1.budget_result_contribution_perc, 0.0)

        self.assertEqual(self.aa_2.budget_result_turnover, 1000.0)
        self.assertEqual(self.aa_2.budget_result_cost, -1500.0)
        self.assertEqual(self.aa_2.budget_result_contribution, -500.0)
        self.assertEqual(self.aa_2.budget_result_contribution_perc, 100.0)

        self.assertEqual(self.aa_3.budget_result_turnover, -1000.0)
        self.assertEqual(self.aa_3.budget_result_cost, -2000.0)
        self.assertEqual(self.aa_3.budget_result_contribution, -3000.0)
        self.assertEqual(self.aa_3.budget_result_contribution_perc, 0.0)

    def test_05_unlink(self):

        self.aa_line_1_1.unlink()
        self.aa_line_2_1.unlink()
        self.aa_line_3_1.unlink()

        self.assertEqual(self.aa_1.budget_result_turnover, -1000.0)
        self.assertEqual(self.aa_1.budget_result_cost, 0.0)
        self.assertEqual(self.aa_1.budget_result_contribution, -1000.0)
        self.assertEqual(self.aa_1.budget_result_contribution_perc, -200.0)

        self.assertEqual(self.aa_2.budget_result_turnover, 0.0)
        self.assertEqual(self.aa_2.budget_result_cost, -1500.0)
        self.assertEqual(self.aa_2.budget_result_contribution, -1500.0)
        self.assertEqual(self.aa_2.budget_result_contribution_perc, 300.0)

        self.assertEqual(self.aa_3.budget_result_turnover, -1000.0)
        self.assertEqual(self.aa_3.budget_result_cost, -1000.0)
        self.assertEqual(self.aa_3.budget_result_contribution, -2000.0)
        self.assertEqual(self.aa_3.budget_result_contribution_perc, 0.0)
