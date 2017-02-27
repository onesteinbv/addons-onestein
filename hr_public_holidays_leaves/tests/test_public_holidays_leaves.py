# -*- coding: utf-8 -*-
# ©  2015 Salton Massally <smassally@idtlabs.sl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common


class TestPublicHolidaysLeave(common.TransactionCase):

    def setUp(self):
        super(TestPublicHolidaysLeave, self).setUp()
        self.holiday_model = self.env["hr.holidays.public"]
        self.holiday_model_line = self.env["hr.holidays.public.line"]
        self.employee_model = self.env['hr.employee']

        # Create holidays
        self.holiday1 = self.holiday_model.create({
            'year': 1995,
        })
        for dt in ['1995-10-14', '1995-12-31', '1995-01-01']:
            self.holiday_model_line.create({
                'name': 'holiday x',
                'date': dt,
                'year_id': self.holiday1.id
            })
        self.holiday2 = self.holiday_model.create({
            'year': 1994,
            'country_id': self.env.ref('base.sl').id
        })
        self.holiday_model_line.create({
            'name': 'holiday 5',
            'date': '1994-10-14',
            'year_id': self.holiday2.id
        })
        self.holiday3 = self.holiday_model.create({
            'year': 1994,
            'country_id': self.env.ref('base.sk').id
        })
        self.holiday_model_line.create({
            'name': 'holiday 6',
            'date': '1994-11-14',
            'year_id': self.holiday3.id
        })

        self.employee = self.employee_model.create(
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

    def test_01_validate(self):
        self.holiday2.validate()
        self.assertEqual(self.holiday2.state, 'validate')

    def test_02_reset(self):
        self.holiday2.validate()
        self.holiday2.reset()
        self.assertEqual(self.holiday2.state, 'draft')
