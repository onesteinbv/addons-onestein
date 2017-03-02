# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class TestHolidaysStatusExpiration(common.TransactionCase):
    def setUp(self):
        super(TestHolidaysStatusExpiration, self).setUp()
        self.Employee = self.env['hr.employee']
        self.Status = self.env['hr.holidays.status']
        today = date.today().strftime(DF)

        self.employee_1 = self.Employee.create({
            'name': 'Employee 1',
        })

        self.status_1 = self.Status.create({
            'name': 'Status 1',
            'limit': False,
        })

        self.status_2 = self.Status.create({
            'name': 'Status 2',
            'limit': False,
            'expiration_date': today,
        })

    def test_01_name_get(self):
        name1 = self.status_1.name_get()
        self.assertEquals(name1[0][1], 'Status 1')
        name1 = self.status_1.with_context(
            employee_id=self.employee_1.id).name_get()
        self.assertEquals(
            name1[0][1],
            'Status 1  (0.0 Left / 0.0 Virtually Left)')

        name2 = self.status_2.name_get()
        self.assertEquals(name2[0][1], 'Status 2')
        name2 = self.status_2.with_context(
            employee_id=self.employee_1.id).name_get()
        tst_name = 'Status 2  (0.0 Left / 0.0 Virtually Left - Exp. Date '
        tst_name += '%s)' % self.status_2.expiration_date
        self.assertEquals(
            name2[0][1],
            tst_name
        )

    def test_dummy(self):
        None
