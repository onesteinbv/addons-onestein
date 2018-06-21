# Copyright 2017-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF


class TestHRAbsenteeismHours(common.TransactionCase):
    def setUp(self):
        super(TestHRAbsenteeismHours, self).setUp()

        self.Holidays = self.env['hr.holidays']
        self.HolidaysStatus = self.env['hr.holidays.status']
        self.Employee = self.env['hr.employee']

        self.start = (datetime.today() - relativedelta(days=1)).replace(
            hour=8, minute=0, second=0)
        self.end = (datetime.today() - relativedelta(days=1)).replace(
            hour=18, minute=0, second=0)

        start = self.start.strftime(DF)
        end = self.end.strftime(DF)

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
            'date_from': start,
            'date_to': end,
            'employee_id': self.employee_1.id,
        })

    def test_01_increase_date_to(self):
        self.Holidays.increase_date_to()
