# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    related_ids = fields.One2many(
        'hr.employee.related',
        'employee_id',
        string='Related'
    )
