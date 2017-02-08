# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Onestein (<http://www.onestein.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields


class hr_employee_related(models.Model):
    _name = 'hr.employee.related'
    _description = 'Employee related'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    name = fields.Char("First name")
    last_name = fields.Char("Last name")
    birth_name = fields.Char("Birth name")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string='Gender')
    relation = fields.Char("Employee relation")
    bsn_number = fields.Char("BSN")
    birth_date = fields.Date(string="Birth date")
    telephone = fields.Char("Telephone")
    note = fields.Text("Note")


class hr_employee(models.Model):
    _inherit = 'hr.employee'

    related_ids = fields.One2many('hr.employee.related', 'employee_id',
                                  string='Related')
