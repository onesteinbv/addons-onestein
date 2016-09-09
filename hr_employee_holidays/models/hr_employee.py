# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class hr_employee(models.Model):
    _inherit = "hr.employee"

    holiday_ids = fields.One2many('hr.holidays', 'employee_id', string='Holidays')
