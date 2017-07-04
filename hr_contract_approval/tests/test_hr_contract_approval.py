# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class TestHRContractApproval(common.TransactionCase):

    def setUp(self):
        super(TestHRContractApproval, self).setUp()
        self.Contract = self.env['hr.contract']
        self.Employee = self.env['hr.employee']

        self.long_time_ago = date.today() - relativedelta(days=100)
        self.time_ago = date.today() - relativedelta(days=10)
        long_time_ago = self.long_time_ago.strftime(DF)
        time_ago = self.time_ago.strftime(DF)

        self.employee_1 = self.Employee.create({
            'name': 'Employee 1',
        })

        self.employee_2 = self.Employee.create({
            'name': 'Employee 1',
        })

        self.contract_1 = self.Contract.create({
            'name': 'Contract 1',
            'employee_id': self.employee_1.id,
            'wage': 2000.0,
            'date_start': long_time_ago,
            'date_end': time_ago,
        })

        self.contract_2 = self.Contract.create({
            'name': 'Contract 2',
            'employee_id': self.employee_2.id,
            'wage': 2000.0,
            'date_start': long_time_ago,
        })

    def test_01_action_request_approval(self):
        self.contract_1.action_request_approval()
        self.assertEqual('wait_approval', self.contract_1.state)

    def test_02_action_approve(self):
        self.contract_1.action_approve()
        self.assertEqual('open', self.contract_1.state)

    def test_03_action_disapprove(self):
        self.contract_1.action_disapprove()
        self.assertEqual('close', self.contract_1.state)

    def test_04_action_reset_to_new(self):
        self.contract_1.action_reset_to_new()
        self.assertEqual('draft', self.contract_1.state)

    def test_05_check_expiring(self):
        self.contract_1.action_approve()
        self.contract_2.action_approve()
        self.Contract.check_expiring()
        self.assertEqual('close', self.contract_1.state)
        self.assertEqual('open', self.contract_2.state)

    def test_06_check_to_renew(self):
        self.contract_1.action_approve()
        self.contract_2.action_approve()
        self.Contract.check_to_renew()
        self.assertEqual('pending', self.contract_1.state)
        self.assertEqual('open', self.contract_2.state)

    def test_07_check_write(self):
        self.contract_1.action_approve()
        self.contract_1.write({'wage': 1000.0})
        self.assertEqual('draft', self.contract_1.state)
