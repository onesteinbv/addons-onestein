# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
from odoo.exceptions import Warning
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF


class TestPublicHolidaysLeave(common.TransactionCase):

    def setUp(self):
        super(TestPublicHolidaysLeave, self).setUp()
        self.Leave = self.env['hr.holidays']
        self.Category = self.env['hr.employee.category']
        self.HolidaysStatus = self.env['hr.holidays.status']
        self.Public = self.env["hr.holidays.public"]
        self.PublicLine = self.env["hr.holidays.public.line"]
        self.Employee = self.env['hr.employee']
        self.Calendar = self.env['resource.calendar']
        self.Workday = self.env['resource.calendar.attendance']

        self.today_start = datetime.today().replace(
            hour=8, minute=0, second=0, microsecond=0)
        self.today_end = datetime.today().replace(
            hour=18, minute=0, second=0, microsecond=0)

        today_start = self.today_start.strftime(DF)
        today_end = self.today_end.strftime(DF)

        yesterday_start = self.today_start - relativedelta(days=1)
        yesterday_end = self.today_end - relativedelta(days=1)

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

        self.category_1 = self.Category.create({
            'name': 'Category 1',
        })

        self.employee_1 = self.Employee.create(
            {
                'name': 'Employee 1',
                'calendar_id': self.calendar.id,
                'address_id': self.env['res.partner'].create(
                    {
                        'name': 'Employee 1',
                        'country_id': self.env.ref('base.sl').id
                    }
                ).id
            }
        )
        self.employee_2 = self.Employee.create(
            {
                'name': 'Employee 2',
                'calendar_id': self.calendar.id,
                'address_id': self.env['res.partner'].create(
                    {
                        'name': 'Employee 2',
                        'country_id': self.env.ref('base.sl').id
                    }
                ).id
            }
        )

        self.status_1 = self.HolidaysStatus.create({
            'name': 'Status 1',
            'limit': True,
        })

        # Create holidays
        self.holiday1 = self.Public.create({
            'year': 1995,
        })
        for dt in ['1995-10-14', '1995-12-31', '1995-01-01']:
            self.PublicLine.create({
                'name': 'holiday x',
                'date': dt,
                'year_id': self.holiday1.id
            })
        self.holiday2 = self.Public.create({
            'year': 1994,
            'country_id': self.env.ref('base.sl').id
        })
        self.PublicLine.create({
            'name': 'holiday 5',
            'date': '1994-10-14',
            'year_id': self.holiday2.id
        })
        self.holiday3 = self.Public.create({
            'year': 1994,
            'country_id': self.env.ref('base.sk').id
        })
        self.PublicLine.create({
            'name': 'holiday 6',
            'date': '1994-11-14',
            'year_id': self.holiday3.id
        })

        self.leave_1 = self.Leave.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'remove',
            'date_from': today_start,
            'date_to': today_end,
            'employee_id': self.employee_1.id,
            'public_holiday_id': self.holiday2.line_ids.ids[0],
        })

        self.leave_2 = self.Leave.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'remove',
            'employee_id': self.employee_2.id,
            'public_holiday_id': self.holiday2.line_ids.ids[0],
        })

        self.leave_3 = self.Leave.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'category',
            'type': 'remove',
            'employee_id': None,
            'category_id': self.category_1.id,
            'public_holiday_id': self.holiday2.line_ids.ids[0],
        })

        self.leave_4 = self.Leave.create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'remove',
            'date_from': yesterday_start,
            'date_to': yesterday_end,
            'employee_id': self.employee_1.id,
            'public_holiday_id': self.holiday2.line_ids.ids[0],
        })

    def test_01_validate(self):
        self.holiday2.validate()
        self.assertEqual(self.holiday2.state, 'validate')

    def test_02_reset(self):
        self.holiday2.validate()
        self.holiday2.reset()
        self.assertEqual(self.holiday2.state, 'draft')

    def test_03_exception(self):
        type = self.env.ref('hr_public_holidays_leaves.hr_public_holiday')
        type.unlink()
        with self.assertRaises(Warning):
            self.holiday2.validate()

    def test_04_action_validate1(self):
        self.leave_1.action_validate()

    def test_05_action_validate2(self):
        type = self.env.ref('hr_public_holidays_leaves.hr_public_holiday')
        type.unlink()
        with self.assertRaises(Warning):
            self.leave_2.action_validate()

    def test_06_action_validate3(self):
        self.leave_3.action_validate()

    def test_07_action_validate4(self):
        public_status_id = self.env.ref(
            'hr_public_holidays_leaves.hr_public_holiday')
        self.leave_4.write({
            'holiday_status_id': public_status_id.id})
        self.leave_4.action_validate()
