# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class hr_employee(models.Model):
    _inherit = "hr.employee"

    holiday_ids = fields.One2many(
        'hr.holidays',
        'employee_id',
        string='Holidays'
    )
