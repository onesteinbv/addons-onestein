# Copyright 2017-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF
from odoo.exceptions import UserError


class TestHRAbsenteeism(common.TransactionCase):
    def setUp(self):
        super(TestHRAbsenteeism, self).setUp()

        self.Holidays = self.env['hr.holidays']
        self.HolidaysStatus = self.env['hr.holidays.status']
        self.Employee = self.env['hr.employee']
        self.Notification = self.env['hr.absenteeism.notifications']

        self.start = (datetime.today() - relativedelta(days=1)).replace(
            hour=8, minute=0, second=0)
        self.end = (datetime.today() - relativedelta(days=1)).replace(
            hour=18, minute=0, second=0)

        start = self.start.strftime(DF)
        end = self.end.strftime(DF)

        self.l_start = (self.start + relativedelta(days=2)).strftime(DF)
        self.l_end = (self.end + relativedelta(days=2)).strftime(DF)

        self.employee_1 = self.Employee.create({
            'name': 'Employee 1',
        })
        self.employee_2 = self.Employee.create({
            'name': 'Employee 2',
        })

        self.status_1 = self.HolidaysStatus.create({
            'name': 'Status',
            'limit': True,
            'absenteeism_control': True,
        })

        self.notification_1 = self.Notification.create({
            'name': 'Notification 1',
            'interval': 1,
            'leave_type_id': self.status_1.id,
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

    def test_02_increase_date_to(self):

        self.Holidays.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'remove',
            'date_from': self.l_start,
            'date_to': self.l_end,
            'employee_id': self.employee_2.id,
        })
        with self.assertRaises(UserError):
            self.Holidays.increase_date_to()
