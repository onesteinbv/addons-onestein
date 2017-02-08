# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    @api.model
    def get_employee_calendar(self, employee):
        calendar = super(HrHolidays, self).get_employee_calendar(employee)
        if not calendar:
            if employee.contract_id and employee.contract_id.working_hours:
                calendar = employee.contract_id.working_hours.id
        return calendar
