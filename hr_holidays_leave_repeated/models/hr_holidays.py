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
    def _update_workday_from_to(self, employee, from_dt, to_dt, days):

        user = self.env.user
        orig_from_dt = fields.Datetime.context_timestamp(user, from_dt)
        orig_to_dt = fields.Datetime.context_timestamp(user, to_dt)
        working_hours = self._get_employee_working_hours(employee)
        work_hours = working_hours.get_working_hours(
            from_dt,
            to_dt,
            compute_leaves=True,
            resource_id=employee.resource_id.id,
        )
        while True:
            from_dt = from_dt + relativedelta(days=days)
            to_dt = to_dt + relativedelta(days=days)

            new_work_hours = working_hours.get_working_hours(
                from_dt,
                to_dt,
                compute_leaves=True,
                resource_id=employee.resource_id.id,
            )
            if new_work_hours and work_hours <= new_work_hours:
                break

        user_from_dt = fields.Datetime.context_timestamp(user, from_dt)
        user_to_dt = fields.Datetime.context_timestamp(user, to_dt)
        from_dt = from_dt - user_from_dt.tzinfo._utcoffset
        from_dt = from_dt + orig_from_dt.tzinfo._utcoffset
        to_dt = to_dt - user_to_dt.tzinfo._utcoffset
        to_dt = to_dt + orig_to_dt.tzinfo._utcoffset

        return from_dt, to_dt

    @api.model
    def _update_leave_vals(self, vals, employee):
        vals_dict = self._get_vals_dict()
        param_dict = vals_dict[vals.get('repeat_every')]
        days = param_dict['days']
        error_msg = param_dict['user_error_msg']
        date_from = vals.get('date_from')
        date_to = vals.get('date_to')
        from_dt = fields.Datetime.from_string(date_from)
        to_dt = fields.Datetime.from_string(date_to)
        holiday_duration = self._get_leave_duration(from_dt, to_dt)
        if holiday_duration and holiday_duration.days > days:
            raise UserError(error_msg)
        from_dt, to_dt = self._update_workday_from_to(
            employee, from_dt, to_dt, days)
        vals['date_from'] = fields.Datetime.to_string(from_dt)
        vals['date_to'] = fields.Datetime.to_string(to_dt)
        return vals

    @api.model
    def _get_vals_dict(self):
        vals_dict = {
            'workday': {
                'days': 1,
                'user_error_msg': _(
                    '''The repetition is based on workdays:
                     the duration of the leave request
                     must not exceed 1 day.
                    ''')
            },
            'week': {
                'days': 7,
                'user_error_msg': _(
                    '''The repetition is every week:
                     the duration of the leave request
                     must not exceed 1 week.
                    ''')
            },
            'biweek': {
                'days': 14,
                'user_error_msg': _(
                    '''The repetition is based on 2 weeks:
                     the duration of the leave request
                     must not exceed 2 weeks.
                    ''')
            },
            'month': {
                'days': 28,
                'user_error_msg': _(
                    '''The repetition is every four weeks:
                     the duration of the leave request
                     must not exceed 28 days.
                    ''')
            }
        }
        return vals_dict

    @api.model
    def _get_leave_duration(self, from_dt, to_dt):
        holiday_duration = None
        if from_dt and to_dt:
            holiday_duration = to_dt - from_dt
        return holiday_duration

    @api.model
    def _get_employee_working_hours(self, employee):
        working_hours = \
            employee.calendar_id or \
            employee.contract_id and \
            employee.contract_id.working_hours or None
        return working_hours

    @api.model
    def create_handler(self, vals):
        employee = self.env['hr.employee'].browse(vals.get('employee_id'))
        working_hours = self._get_employee_working_hours(employee)
        if working_hours:
            count = 1
            while count < vals.get('repeat_limit', 0):
                vals = self._update_leave_vals(vals, employee)
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
