# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    holiday_ids = fields.One2many(
        'hr.holidays',
        'employee_id',
        string='Holidays'
    )
