# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployeeRelated(models.Model):
    _name = 'hr.employee.related'
    _description = 'Employee related'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    name = fields.Char('First name')
    last_name = fields.Char('Last name')
    birth_name = fields.Char('Birth name')
    gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female')],
        string='Gender'
    )
    relation = fields.Char('Employee relation')
    bsn_number = fields.Char('BSN')
    birth_date = fields.Date('Birth date')
    telephone = fields.Char('Telephone')
    note = fields.Text('Note')
