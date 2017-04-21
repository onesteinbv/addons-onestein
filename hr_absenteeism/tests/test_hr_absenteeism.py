# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning


class TestHRAbsenteeism(common.TransactionCase):
    def setUp(self):
        super(TestHRAbsenteeism, self).setUp()

        self.Holidays = self.env['hr.holidays']
        self.HolidaysStatus = self.env['hr.holidays.status']
        self.Employee = self.env['hr.employee']
        self.Notification = self.env['hr.absenteeism.notifications']

        self.today_start = datetime.today().replace(
            hour=8, minute=0, second=0) - relativedelta(days=1)
        self.today_end = datetime.today().replace(
            hour=18, minute=0, second=0) - relativedelta(days=1)

        today_start = self.today_start.strftime(DF)
        today_end = self.today_end.strftime(DF)

        self.l_start = (self.today_start + relativedelta(days=2)).strftime(DF)
        self.l_end = (self.today_end + relativedelta(days=2)).strftime(DF)

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
            'date_from': today_start,
            'date_to': today_end,
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
        with self.assertRaises(Warning):
            self.Holidays.increase_date_to()
