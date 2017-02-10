# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF
from odoo.exceptions import Warning


class TestLeaveHours(common.TransactionCase):
    def setUp(self):
        super(TestLeaveHours, self).setUp()

        self.leave_obj = self.env['hr.holidays']
        self.status_obj = self.env['hr.holidays.status']
        self.calendar_obj = self.env['resource.calendar']
        self.workday_obj = self.env['resource.calendar.attendance']
        self.employee_obj = self.env['hr.employee']

        self.today_start = datetime.today().replace(
            hour=8, minute=0, second=0)
        self.today_end = datetime.today().replace(
            hour=18, minute=0, second=0)

        today_start = self.today_start.strftime(DF)
        today_end = self.today_end.strftime(DF)

        self.calendar = self.calendar_obj.create({
            'name': 'Calendar 1',
        })

        for i in range(0, 7):
            self.workday_obj.create({
                'name': 'Day ' + str(i),
                'dayofweek': str(i),
                'hour_from': 8.0,
                'hour_to': 16.0,
                'calendar_id': self.calendar.id,
            })

        self.employee_1 = self.employee_obj.create({
            'name': 'Employee 1',
            'calendar_id': self.calendar.id,
        })
        self.employee_2 = self.employee_obj.create({
            'name': 'Employee 2',
            'calendar_id': self.calendar.id,
        })
        self.employee_3 = self.employee_obj.create({
            'name': 'Failing Employee',
            'calendar_id': self.calendar.id,
        })

        self.status_1 = self.status_obj.create({
            'name': 'Repeating Status',
            'limit': True,
            'repeat': True,
        })

        self.leave_allocation_1 = self.leave_obj.create({
            'name': 'Allocation Request 1',
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'employee_id': self.employee_1.id,
            'number_of_days_temp': 10,
            'type': 'add',
        })

        self.leave_1 = self.leave_obj.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'remove',
            'repeat_every': 'workday',
            'repeat_limit': 5,
            'date_from': today_start,
            'date_to': today_end,
            'employee_id': self.employee_1.id,
        })

        self.leave_allocation_2 = self.leave_obj.create({
            'name': 'Allocation Request 2',
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'employee_id': self.employee_2.id,
            'number_of_days_temp': 10,
            'type': 'add',
        })

        self.leave_2 = self.leave_obj.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'remove',
            'repeat_every': 'week',
            'repeat_limit': 4,
            'date_from': today_start,
            'date_to': today_end,
            'employee_id': self.employee_2.id,
        })

    def test_01_onchange(self):
        field_onchange = self.leave_1._onchange_spec()
        self.assertEqual(field_onchange.get('employee_id'), '1')
        self.assertEqual(field_onchange.get('date_from'), '1')
        self.assertEqual(field_onchange.get('date_to'), '1')

        values = {
            'employee_id': self.employee_1.id,
            'date_from': self.today_start.strftime(DF),
            'date_to': self.today_end.strftime(DF),
        }
        self.leave_1.onchange(values, 'employee_id', field_onchange)
        self.leave_1.onchange(values, 'date_from', field_onchange)
        self.leave_1.onchange(values, 'date_to', field_onchange)

        field_onchange = self.leave_allocation_1._onchange_spec()
        self.leave_allocation_1.with_context(default_type='add').onchange(
            values, 'employee_id', field_onchange)
        self.leave_allocation_1.with_context(default_type='add').onchange(
            values, 'date_from', field_onchange)
        self.leave_allocation_1.with_context(default_type='add').onchange(
            values, 'date_to', field_onchange)

    def test_02_onchange_fail(self):

        field_onchange = self.leave_1._onchange_spec()
        values = {
            'date_from': self.today_end.strftime(DF),
            'date_to': self.today_start.strftime(DF),
        }

        with self.assertRaises(Warning):
            self.leave_1.onchange(values, 'date_from', field_onchange)

        with self.assertRaises(Warning):
            self.leave_1.onchange(values, 'date_to', field_onchange)
