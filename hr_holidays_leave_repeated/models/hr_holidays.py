# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class HrHolidays(models.Model):
    _inherit = "hr.holidays"

    repeat_every = fields.Selection([
        ('workday', 'Every workday'),
        ('week', 'Every week'),
        ('biweek', 'Every two weeks'),
        ('month', 'Every four weeks')],
        string='Repeat Every'
    )
    holiday_type_repeat = fields.Boolean(
        related='holiday_status_id.repeat',
        string='Repeating'
    )
    repeat_limit = fields.Integer(
        default=1,
        string='Repeat # times'
    )

    @api.model
    def _get_workday_vals(
            self, vals, employee, working_hours,
            from_dt, to_dt, work_hours, diff
    ):
        while True:
            from_dt = from_dt + relativedelta(days=1)
            to_dt = to_dt + relativedelta(days=1)
            new_work_hours = working_hours.get_working_hours(
                from_dt,
                to_dt,
                compute_leaves=True,
                resource_id=employee.resource_id.id,
            )
            if new_work_hours and work_hours <= new_work_hours:
                break
        vals['date_from'] = fields.Datetime.to_string(from_dt - diff)
        vals['date_to'] = fields.Datetime.to_string(to_dt - diff)
        return vals

    @api.model
    def _get_week_vals(
            self, vals, employee, working_hours,
            from_dt, to_dt, work_hours, diff
    ):
        while True:
            from_dt = from_dt + relativedelta(days=7)
            to_dt = to_dt + relativedelta(days=7)
            new_work_hours = working_hours.get_working_hours(
                from_dt,
                to_dt,
                compute_leaves=True,
                resource_id=employee.resource_id.id,
            )
            if new_work_hours and work_hours <= new_work_hours:
                break
        vals['date_from'] = fields.Datetime.to_string(from_dt - diff)
        vals['date_to'] = fields.Datetime.to_string(to_dt - diff)
        return vals

    @api.model
    def _get_biweek_vals(
            self, vals, employee, working_hours,
            from_dt, to_dt, work_hours, diff
    ):
        while True:
            from_dt = from_dt + relativedelta(days=14)
            to_dt = to_dt + relativedelta(days=14)
            new_work_hours = working_hours.get_working_hours(
                from_dt,
                to_dt,
                compute_leaves=True,
                resource_id=employee.resource_id.id,
            )
            if new_work_hours and work_hours <= new_work_hours:
                break
        vals['date_from'] = fields.Datetime.to_string(from_dt - diff)
        vals['date_to'] = fields.Datetime.to_string(to_dt - diff)
        return vals

    @api.model
    def _get_month_vals(
            self, vals, employee, working_hours,
            from_dt, to_dt, work_hours, diff
    ):
        while True:
            from_dt = from_dt + relativedelta(days=28)
            to_dt = to_dt + relativedelta(days=28)
            new_work_hours = working_hours.get_working_hours(
                from_dt,
                to_dt,
                compute_leaves=True,
                resource_id=employee.resource_id.id,
            )
            if new_work_hours and work_hours <= new_work_hours:
                break
        vals['date_from'] = fields.Datetime.to_string(from_dt - diff)
        vals['date_to'] = fields.Datetime.to_string(to_dt - diff)
        return vals

    @api.model
    def create_handler(self, vals):
        count = 1
        while count < vals.get('repeat_limit', 0):
            date_from = vals.get('date_from')
            date_to = vals.get('date_to')
            employee = self.env['hr.employee'].browse(vals.get('employee_id'))
            working_hours = employee.calendar_id
            working_hours = \
                working_hours or \
                employee.contract_id and \
                employee.contract_id.working_hours or None
            if working_hours:
                user = self.env.user
                from_dt = fields.Datetime.from_string(date_from)
                from_dt_orig = from_dt.replace(tzinfo=None)
                from_dt = fields.Datetime.context_timestamp(user, from_dt)
                from_dt = from_dt.replace(tzinfo=None)
                diff = from_dt - from_dt_orig
                to_dt = None
                holiday_duration = None
                if date_to and date_from:
                    to_dt = fields.Datetime.from_string(date_to)
                    to_dt = fields.Datetime.context_timestamp(user, to_dt)
                    to_dt = to_dt.replace(tzinfo=None)
                    holiday_duration = to_dt - from_dt
                work_hours = working_hours. \
                    get_working_hours(from_dt,
                                      to_dt,
                                      compute_leaves=True,
                                      resource_id=employee.resource_id.id,
                                      )
                if vals.get('repeat_every') == 'workday':
                    if holiday_duration and holiday_duration.days > 1:
                        raise UserError(
                            _('''The repetition is based on workdays:
                             the duration of the leave request
                             must not exceed 1 day.
                            '''))
                    vals = self._get_workday_vals(
                        vals, employee, working_hours,
                        from_dt, to_dt, work_hours, diff
                    )
                elif vals.get('repeat_every') == 'week':
                    if holiday_duration and holiday_duration.days > 7:
                        raise UserError(
                            _('''The repetition is every week:
                             the duration of the leave request
                             must not exceed 1 week.
                            '''))
                    vals = self._get_week_vals(
                        vals, employee, working_hours,
                        from_dt, to_dt, work_hours, diff
                    )
                elif vals.get('repeat_every') == 'biweek':
                    if holiday_duration and holiday_duration.days > 14:
                        raise UserError(
                            _('''The repetition is based on 2 weeks:
                             the duration of the leave request
                             must not exceed 2 weeks.
                            '''))
                    vals = self._get_biweek_vals(
                        vals, employee, working_hours,
                        from_dt, to_dt, work_hours, diff
                    )
                elif vals.get('repeat_every') == 'month':
                    if holiday_duration and holiday_duration.days > 28:
                        raise UserError(
                            _('''The repetition is every four weeks:
                             the duration of the leave request
                             must not exceed 28 days.
                            '''))
                    vals = self._get_month_vals(
                        vals, employee, working_hours,
                        from_dt, to_dt, work_hours, diff
                    )
                self.with_context({
                    "skip_create_handler": True
                }).create(vals)
            count += 1

    @api.model
    def create(self, vals):
        res = super(HrHolidays, self).create(vals)
        skip_create_handler = self._context.get('skip_create_handler')
        if not skip_create_handler:
            self.create_handler(vals)
        return res

    @api.constrains('repeat_limit')
    def _check_repeat_limit(self):
        for record in self:
            if record.repeat_limit < 0:
                raise UserError(
                    _('Please, set a positive repeating # of times limit.'))
