# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning


class TestHRAbsenteeismHours(common.TransactionCase):
    def setUp(self):
        super(TestHRAbsenteeismHours, self).setUp()

        self.Holidays = self.env['hr.holidays']
        self.HolidaysStatus = self.env['hr.holidays.status']
        self.Employee = self.env['hr.employee']

        self.today_start = datetime.today().replace(
            hour=8, minute=0, second=0)
        self.today_end = datetime.today().replace(
            hour=18, minute=0, second=0)

        today_start = self.today_start.strftime(DF)
        today_end = self.today_end.strftime(DF)

        self.employee_1 = self.Employee.create({
            'name': 'Employee 1',
        })

        self.status_1 = self.HolidaysStatus.create({
            'name': 'Status',
            'limit': True,
            'absenteeism_control': True,
        })

        self.leave_1 = self.Holidays.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'remove',
            'date_from': today_start,
            'date_to': today_end,
            'employee_id': self.employee_1.id,
        })

    def test_01_increase_date_to(self):
        self.Holidays.increase_date_to()
