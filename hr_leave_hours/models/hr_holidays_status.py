# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class hr_holidays_status(models.Model):
    _inherit = "hr.holidays.status"

    @api.model
    def get_hours(self, employee_id):
        result = {
            'max_hours': 0,
            'remaining_hours': 0,
            'hours_taken': 0,
            'virtual_remaining_hours': 0,
        }

        holiday_ids = self.env['hr.employee'].browse(
            employee_id
        ).holiday_ids.filtered(
            lambda x: x.state in [
                'confirm',
                'validate1',
                'validate'
            ] and x.holiday_status_id == self)

        for holiday in holiday_ids:

            sign = 1
            if holiday.type == 'remove':
                sign = -1

            result['virtual_remaining_hours'] += (holiday.number_of_hours_temp * sign)
            if holiday.state == 'validate':
                result['remaining_hours'] += (holiday.number_of_hours_temp * sign)
                if sign > 0:
                    result['max_hours'] += holiday.number_of_hours_temp
                else:
                    result['hours_taken'] += holiday.number_of_hours_temp

        return result

    @api.multi
    def _user_left_hours(self):
        employee_id = self._context.get('employee_id', False)
        if not employee_id:
            employees = self.env['hr.employee'].search([
                ('user_id', '=', self._uid)
            ], limit=1)
            if employees:
                employee_id = employees.id
        for status in self:
            if employee_id:
                res = status.get_hours(employee_id)
                status.hours_taken = res['hours_taken']
                status.remaining_hours = res['remaining_hours']
                status.max_hours = res['max_hours']
                status.virtual_remaining_hours = res[
                    'virtual_remaining_hours'
                ]
            else:
                status.hours_taken = 0
                status.remaining_hours = 0
                status.max_hours = 0
                status.virtual_remaining_hours = 0

    max_hours = fields.Float(
        compute="_user_left_hours",
        string='Maximum Allowed Hours'
    )
    hours_taken = fields.Float(
        compute="_user_left_hours",
        string='Hours Already Taken'
    )
    remaining_hours = fields.Float(
        compute="_user_left_hours",
        string='Remaining Hours'
    )
    virtual_remaining_hours = fields.Float(
        compute="_user_left_hours",
        string='Virtual Remaining Hours'
    )

    @api.multi
    def name_get(self):
        if not self._context.get('employee_id', False):
            # leave counts is based on employee_id, would be
            # inaccurate if not based on correct employee
            return super(hr_holidays_status, self).name_get()

        res = []
        for record in self:
            name = record.name
            if not record.limit:
                name += ('  (%.1f Left)' % (
                    record.max_hours-record.hours_taken
                ))
            res.append((record.id, name))
        return res
