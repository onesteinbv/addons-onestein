# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    @api.depends('user_id')
    def _fnct_display_personal_data(self):
        for employee in self:
            employee.fnct_display_personal_data = False
            if self.user_has_groups('hr.group_hr_user'):
                employee.fnct_display_personal_data = True
            elif employee.user_id == self.env.user:
                employee.fnct_display_personal_data = True

    fnct_display_personal_data = fields.Boolean(
        compute='_fnct_display_personal_data'
    )
