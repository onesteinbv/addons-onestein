# Copyright 2017-2019 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, date
from odoo.tests import common


class TestHolidaysExpiration(common.TransactionCase):
    def setUp(self):
        super(TestHolidaysExpiration, self).setUp()

        today_start = datetime.today().replace(
            hour=8, minute=0, second=0)
        today_end = datetime.today().replace(
            hour=18, minute=0, second=0)

        self.employee_1 = self.env['hr.employee'].create({
            'name': 'Employee 1',
        })

        self.status_1 = self.env['hr.leave.type'].create({
            'name': 'Leave Status',
            'allocation_type': 'fixed_allocation',
        })

        self.leave_1 = self.env['hr.leave'].create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'date_from': today_start,
            'date_to': today_end,
            'employee_id': self.employee_1.id,
        })

        self.allocation_1 = self.env['hr.leave.allocation'].create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'date_from': today_start,
            'date_to': today_end,
            'employee_id': self.employee_1.id,
        })

    def test_01_validate(self):
        self.leave_1.action_approve()
        self.assertEqual(self.leave_1.approval_date.date(), date.today())

        self.allocation_1.action_approve()
        self.assertEqual(self.allocation_1.approval_date.date(), date.today())

    def test_02_action_draft(self):
        self.leave_1.action_approve()
        self.leave_1.action_refuse()
        self.leave_1.action_draft()
        self.assertFalse(self.leave_1.approval_date)

        self.allocation_1.action_approve()
        self.allocation_1.action_refuse()
        self.allocation_1.action_draft()
        self.assertFalse(self.allocation_1.approval_date)
