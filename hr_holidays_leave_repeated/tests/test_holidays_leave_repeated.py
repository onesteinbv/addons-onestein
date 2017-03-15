# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF
from odoo.exceptions import ValidationError, UserError


class TestHolidaysLeaveRepeated(common.TransactionCase):
    def setUp(self):
        super(TestHolidaysLeaveRepeated, self).setUp()

        self.Holidays = self.env['hr.holidays']
        self.HolidaysStatus = self.env['hr.holidays.status']
        self.Calendar = self.env['resource.calendar']
        self.Workday = self.env['resource.calendar.attendance']
        self.Employee = self.env['hr.employee']

        self.today_start = datetime(2016, 12, 1, 8, 0, 0, 0)
        self.today_end = datetime(2016, 12, 1, 18, 0, 0, 0)

        today_start = self.today_start.strftime(DF)
        today_end = self.today_end.strftime(DF)

        self.calendar = self.Calendar.create({
            'name': 'Calendar 1',
        })

        for i in range(0, 7):
            self.Workday.create({
                'name': 'Day ' + str(i),
                'dayofweek': str(i),
                'hour_from': 8.0,
                'hour_to': 16.0,
                'calendar_id': self.calendar.id,
            })

        self.employee_1 = self.Employee.create({
            'name': 'Employee 1',
            'calendar_id': self.calendar.id,
        })
        self.employee_2 = self.Employee.create({
            'name': 'Employee 2',
            'calendar_id': self.calendar.id,
        })
        self.employee_3 = self.Employee.create({
            'name': 'Employee 3',
            'calendar_id': self.calendar.id,
        })
        self.employee_4 = self.Employee.create({
            'name': 'Employee 4',
            'calendar_id': self.calendar.id,
        })
        self.employee_5 = self.Employee.create({
            'name': 'Failing Employee',
            'calendar_id': self.calendar.id,
        })

        self.status_1 = self.HolidaysStatus.create({
            'name': 'Repeating Status',
            'limit': True,
            'repeat': True,
        })

        self.leave_1 = self.Holidays.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'remove',
            'repeat_every': 'workday',
            'repeat_limit': 5,
            'date_from': today_start,
            'date_to': today_end,
            'employee_id': self.employee_1.id,
        })
        self.leave_2 = self.Holidays.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'remove',
            'repeat_every': 'week',
            'repeat_limit': 4,
            'date_from': today_start,
            'date_to': today_end,
            'employee_id': self.employee_2.id,
        })
        self.leave_3 = self.Holidays.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'remove',
            'repeat_every': 'biweek',
            'repeat_limit': 3,
            'date_from': today_start,
            'date_to': today_end,
            'employee_id': self.employee_3.id,
        })
        self.leave_4 = self.Holidays.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'remove',
            'repeat_every': 'month',
            'repeat_limit': 2,
            'date_from': today_start,
            'date_to': today_end,
            'employee_id': self.employee_4.id,
        })

    def test_01_count_repetitions(self):

        leave_1_list = self.Holidays.search(
            [('holiday_status_id', '=', self.status_1.id),
             ('employee_id', '=', self.employee_1.id)])
        leave_2_list = self.Holidays.search(
            [('holiday_status_id', '=', self.status_1.id),
             ('employee_id', '=', self.employee_2.id)])
        leave_3_list = self.Holidays.search(
            [('holiday_status_id', '=', self.status_1.id),
             ('employee_id', '=', self.employee_3.id)])
        leave_4_list = self.Holidays.search(
            [('holiday_status_id', '=', self.status_1.id),
             ('employee_id', '=', self.employee_4.id)])

        self.assertEqual(len(leave_1_list.ids), 5)
        self.assertEqual(len(leave_2_list.ids), 4)
        self.assertEqual(len(leave_3_list.ids), 3)
        self.assertEqual(len(leave_4_list.ids), 2)

    def test_02_workdays(self):
        for i in range(0, 5):
            check_from = (self.today_start + timedelta(days=i)).strftime(DF)
            check_to = (self.today_end + timedelta(days=i)).strftime(DF)
            self.assertEqual(len(self.Holidays.search(
                [('holiday_status_id', '=', self.status_1.id),
                 ('employee_id', '=', self.employee_1.id),
                 ('date_from', '=', check_from),
                 ('date_to', '=', check_to)]
            ).ids), 1)

    def test_03_weeks(self):

        for i in range(0, 4):
            check_from = (self.today_start + timedelta(
                days=i * 7)).strftime(DF)
            check_to = (self.today_end + timedelta(days=i * 7)).strftime(DF)
            self.assertEqual(len(self.Holidays.search(
                [('holiday_status_id', '=', self.status_1.id),
                 ('employee_id', '=', self.employee_2.id),
                 ('date_from', '=', check_from),
                 ('date_to', '=', check_to)]
            ).ids), 1)

    def test_04_biweeks(self):
        for i in range(0, 3):
            check_from = (self.today_start + timedelta(
                days=i * 14)).strftime(DF)
            check_to = (self.today_end + timedelta(days=i * 14)).strftime(DF)
            self.assertEqual(len(self.Holidays.search(
                [('holiday_status_id', '=', self.status_1.id),
                 ('employee_id', '=', self.employee_3.id),
                 ('date_from', '=', check_from),
                 ('date_to', '=', check_to)]
            ).ids), 1)

    def test_05_months(self):
        for i in range(0, 2):
            check_from = (self.today_start + timedelta(
                days=i * 28)).strftime(DF)
            check_to = (self.today_end + timedelta(days=i * 28)).strftime(DF)
            self.assertEqual(len(self.Holidays.search(
                [('holiday_status_id', '=', self.status_1.id),
                 ('employee_id', '=', self.employee_4.id),
                 ('date_from', '=', check_from),
                 ('date_to', '=', check_to)]
            ).ids), 1)

    def test_06_check_dates(self):
        with self.assertRaises(ValidationError):
            self.Holidays.create({
                'holiday_status_id': self.status_1.id,
                'holiday_type': 'employee',
                'type': 'remove',
                'repeat_every': 'workday',
                'repeat_limit': -1,
                'date_from': self.today_start.strftime(DF),
                'date_to': self.today_end.strftime(DF),
                'employee_id': self.employee_5.id,
            })

    def test_07_check_dates(self):
        with self.assertRaises(UserError):
            self.Holidays.create({
                'holiday_status_id': self.status_1.id,
                'holiday_type': 'employee',
                'type': 'remove',
                'repeat_every': 'workday',
                'repeat_limit': 5,
                'date_from': self.today_start.strftime(DF),
                'date_to': (self.today_end + timedelta(days=2)).strftime(DF),
                'employee_id': self.employee_5.id,
            })
