# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestAlignFollowers(common.TransactionCase):

    def setUp(self):
        super(TestAlignFollowers, self).setUp()

        AnalyticAccount = self.env['account.analytic.account']
        Project = self.env['project.project']

        self.aa_1 = AnalyticAccount.create({
            'name': 'Analytic Account 1',
        })

        self.proj_1 = Project.create({
            'name': 'Project 1',
            'analytic_account_id': self.aa_1.id,
        })

    def test_01_unlink_proj(self):
        self.proj_1.unlink()

    def test_02_unlink_aa(self):
        self.aa_1.unlink()

    def test_03_aa_foll_create(self):
        self.env['mail.followers'].create({
            'res_model': 'account.analytic.account',
            'res_id': self.aa_1.id,
            'partner_id': self.env.ref('base.res_partner_2').id,
        })

    def test_04_proj_foll_create(self):
        self.env['mail.followers'].create({
            'res_model': 'project.project',
            'res_id': self.proj_1.id,
            'partner_id': self.env.ref('base.res_partner_2').id,
        })
