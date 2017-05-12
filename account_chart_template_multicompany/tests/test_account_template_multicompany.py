# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestAccountTemplateMulticompany(common.TransactionCase):

    def setUp(self):
        super(TestAccountTemplateMulticompany, self).setUp()

        self.Template = self.env['account.chart.template']
        self.AccTemplate = self.env['account.account.template']

        self.receivable = self.env.ref('account.data_account_type_receivable')

        self.acc_template = self.AccTemplate.create({
            'name': 'Test 1',
            'code': '000',
            'user_type_id': self.receivable.id,
        })

        self.template = self.Template.create({
            'name': 'Test Template',
            'company_id': self.env.user.company_id.id,
            'currency_id': self.env.user.company_id.currency_id.id,
            'transfer_account_id': self.acc_template.id,
        })

    # def test_01_loading_for_current_company(self):
    #     self.env.user.company_id.write({'chart_template_id': None})
    #     self.template.try_loading_for_current_company()
