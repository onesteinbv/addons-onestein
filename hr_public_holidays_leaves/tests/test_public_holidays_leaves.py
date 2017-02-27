# -*- coding: utf-8 -*-
# ©  2015 Salton Massally <smassally@idtlabs.sl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF
from odoo.exceptions import Warning


class TestPublicHolidaysLeave(common.TransactionCase):

    def setUp(self):
        super(TestPublicHolidaysLeave, self).setUp()
        self.Leave = self.env['hr.holidays']
        self.Category = self.env['hr.employee.category']
        self.HolidaysStatus = self.env['hr.holidays.status']
        self.Public = self.env["hr.holidays.public"]
        self.PublicLine = self.env["hr.holidays.public.line"]
        self.Employee = self.env['hr.employee']

        self.category_1 = self.Category.create({
            'name': 'Category 1',
        })

        self.employee_1 = self.Employee.create(
            {
                'name': 'Employee 1',
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
