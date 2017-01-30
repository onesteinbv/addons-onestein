# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class HrEmployee(models.Model):

    _inherit = 'hr.employee'

    employee_number = fields.Char(copy=False)

    @api.model
    def create(self, vals):

        def get_employee_sequence(Sequence):
            number = Sequence.next_by_code('hr.employee') or '/'
            return number

        if vals.get('employee_number'):
            searching = True
            while searching:
                number = get_employee_sequence(self.env['ir.sequence'])
                if not self.search([
                    ('employee_number', '=', number)
                ], limit=1):
                    vals['employee_number'] = number
                    searching = False
        return super(HrEmployee, self).create(vals)

    _sql_constraints = [
        ('employee_number',
         'unique (employee_number)',
         'Employee Number must be unique !')
    ]
