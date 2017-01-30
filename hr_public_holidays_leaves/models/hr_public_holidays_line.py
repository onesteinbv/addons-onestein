# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime
import logging

from odoo import api, models
from odoo.exceptions import Warning
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class HrHolidaysPublicLine(models.Model):
    _inherit = 'hr.holidays.public.line'

    @api.model
    def holiday_vals_hook(self, vals, emp):
        return vals

    @api.multi
    def reinit(self):

        def validate(new):
            for leave in new:
                for sig in ('confirm', 'validate', 'second_validate'):
                    leave.signal_workflow(sig)

        def unlink_existing(existing):
            for leave in existing:
                for sig in ('refuse', 'reset'):
                    leave.signal_workflow(sig)
                leave.unlink()

        def get_matches_existing(existing, matches):
            existing = [h for h in existing if h not in matches]
            return existing

        def get_matches(emp, existing, holiday_line):
            matches = [h for h in existing
                       if h.employee_id.id == emp.id and
                       h.public_holiday_id.id == holiday_line.id]
            return matches

        def get_leave_type(Data):
            try:
                res = Data.get_object(
                    'hr_public_holidays_leaves', 'hr_public_holiday')
            except ValueError:
                raise Warning(
                    _("Leave Type for Public Holiday not found!"))
            return res.id

        def get_employees(Employee, company):
            company_id = company and company.id or None
            employees = Employee.search(
                ['|',
                 ('company_id', '=', company_id),
                 ('company_id', '=', False)])
            return employees

        def init_vals(emp_id, holiday_line, res_id):
            date_tz_start = datetime.datetime.strptime(
                holiday_line.date,
                "%Y-%m-%d")
            date_tz_stop = datetime.datetime.strptime(
                holiday_line.date,
                "%Y-%m-%d")
            holiday_line_date_from = date_tz_start.strftime(
                '%Y-%m-%d 06:00:00'
            )
            holiday_line_date_to = date_tz_stop.strftime(
                '%Y-%m-%d 19:00:00'
            )
            vals = {
                'name': holiday_line.name,
                'type': 'remove',
                'holiday_type': 'employee',
                'holiday_status_id': res_id,
                'date_from': holiday_line_date_from,
                'date_to': holiday_line_date_to,
                'employee_id': emp_id,
                'public_holiday_id': holiday_line.id
            }
            return vals

        res_id = get_leave_type(self.env['ir.model.data'])

        employees = get_employees(
            self.env['hr.employee'],
            self._context.get('company_id', False)
        )

        existing = self.env['hr.holidays'].search(
            [('public_holiday_id', 'in', self.ids)])

        new = []

        for holiday_line in self:
            for emp in employees:
                    matches = get_matches(emp, existing, holiday_line)
                    if matches:
                        existing = get_matches_existing(existing, matches)
                    else:
                        vals = self.init_vals(emp.id, holiday_line, res_id)
                        vals = self.holiday_vals_hook(vals, emp)
                        new_holiday = self.env['hr.holidays'].with_context(
                            tz=('UTC')).create(vals)
                        new_holiday.onchange_date()
                        new_holiday.number_of_hours = \
                            new_holiday.number_of_hours_temp
                        new.append(new_holiday)

        unlink_existing(existing)

        validate(new)

    @api.multi
    def reset(self):
        for line in self:
            for holiday in self.env['hr.holidays'].search(
                    [('public_holiday_id', '=', line.id)]):
                for sig in ('refuse', 'reset'):
                    holiday.signal_workflow(sig)
                holiday.unlink()
