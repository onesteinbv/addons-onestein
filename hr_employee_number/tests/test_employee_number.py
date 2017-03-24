# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestEmployeeNumber(TransactionCase):

    def test_01(self):
        employee = self.env['hr.employee'].create({
            'name': 'Employee',
            'employee_number': '-',
        })

        self.assertNotEqual(employee.employee_number, '-')
