# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestAlignFollowers(common.TransactionCase):

    def setUp(self):
        super(TestAlignFollowers, self).setUp()

        AnalyticAccount = self.env['account.analytic.account']
        Project = self.env['project.project']
        Follower = self.env['mail.followers']

        self.aa_1 = AnalyticAccount.create({
            'name': 'Analytic Account 1',
        })

        self.proj_1 = Project.create({
            'name': 'Project 1',
            'analytic_account_id': self.aa_1.id,
        })

        self.foll_1 = Follower.create({
            'res_model': 'account.analytic.account',
            'res_id': self.aa_1.id,
            'partner_id': self.env.user.partner_id.id,
        })

        self.foll_2 = Follower.create({
            'res_model': 'project.project',
            'res_id': self.proj_1.id,
            'partner_id': self.env.user.partner_id.id,
        })

    def test_01_unlink_proj(self):
        self.proj_1.unlink()

    def test_02_unlink_aa(self):
        self.aa_1.unlink()
