# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import datetime
from odoo import models, api
from odoo.exceptions import Warning
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class HrHolidaysPublicLine(models.Model):
    _inherit = 'hr.holidays.public.line'

    @api.model
    def _get_employees_public_holiday(self, company):
        company_id = company and company.id or None
        employees = self.env['hr.employee'].search(
            ['|',
             ('company_id', '=', company_id),
             ('company_id', '=', False)])
        return employees

    @api.model
    def holiday_vals_hook(self, vals, emp):
        return vals

    @api.multi
    def reinit(self):
        try:
            res_id = self.env['ir.model.data'].get_object(
                'hr_public_holidays_leaves', 'hr_public_holiday').id
        except ValueError:
            raise Warning(
                _("Leave Type for Public Holiday not found!"))
        employees = self._get_employees_public_holiday(
            self._context.get('company_id', False)
        )

        existing = self.env['hr.holidays'].search(
            [('public_holiday_id', 'in', self.ids)])

        new = []

        for holiday_line in self:
            for emp in employees:
                    matches = [h for h in existing
                               if h.employee_id.id == emp.id and
                               h.public_holiday_id.id == holiday_line.id]
                    if matches:
                        existing = [h for h in existing if h not in matches]
                    else:
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
                            'employee_id': emp.id,
                            'public_holiday_id': holiday_line.id
                        }
                        vals = self.holiday_vals_hook(vals, emp)
                        new_holiday = self.env['hr.holidays'].with_context(
                            tz=('UTC')).create(vals)
                        new_holiday.onchange_date()
                        new_holiday.number_of_hours = \
                            new_holiday.number_of_hours_temp
                        new.append(new_holiday)

        for leave in existing:
            for sig in ('refuse', 'reset'):
                leave.signal_workflow(sig)
            leave.unlink()

        for leave in new:
            for sig in ('confirm', 'validate', 'second_validate'):
                leave.signal_workflow(sig)

    @api.multi
    def reset(self):
        for line in self:
            for holiday in self.env['hr.holidays'].search(
                    [('public_holiday_id', '=', line.id)]):
                for sig in ('refuse', 'reset'):
                    holiday.signal_workflow(sig)
                holiday.unlink()
