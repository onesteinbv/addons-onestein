# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError, Warning
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class HrHolidays(models.Model):
    _inherit = "hr.holidays"

    @api.onchange('employee_id')
    def onchange_holiday_employee(self):
        self.department_id = None
        self.number_of_hours_temp = 0.0
        if self.employee_id:
            self._set_number_of_hours_temp()
            self.department_id = self.employee_id.department_id

    @api.onchange('date_from', 'date_to')
    def onchange_date(self):
        # Check in context what form is open: add or remove
        if self.env.context.get('default_type', '') == 'add':
            return

        self._check_dates()
        self._check_employee()
        self._set_number_of_hours_temp()

    @api.multi
    def _set_number_of_hours_temp(self):
        self.ensure_one()
        from_dt = self._compute_datetime(self.date_from)
        to_dt = self._compute_datetime(self.date_to)
        work_hours = self._compute_work_hours(from_dt, to_dt)
        self.number_of_hours_temp = work_hours

    @api.model
    def _compute_datetime(self, date):
        dt = False
        if date:
            reference_date = fields.Datetime.context_timestamp(
                self.env.user,
                datetime(1990, 2, 8, 12)
            )
            dt = fields.Datetime.from_string(date)
            tz_dt = fields.Datetime.context_timestamp(self.env.user, dt)
            dt = dt + tz_dt.tzinfo._utcoffset
            dt = dt - reference_date.tzinfo._utcoffset
        return dt

    @api.multi
    def _check_dates(self):
        self.ensure_one()
        # date_to has to be greater than date_from
        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise Warning(_(
                    'The start date must be anterior to the end date.'
                ))

    @api.multi
    def _check_employee(self):
        self.ensure_one()
        employee = self.employee_id
        if not employee and (self.date_to or self.date_from):
            raise Warning(_('Set an employee first!'))

    @api.multi
    def _compute_work_hours(self, from_dt, to_dt):
        self.ensure_one()
        employee = self.employee_id
        work_hours = 0.0
        if self.date_from and self.date_to:
            working_hours = self._get_working_hours(employee)
            if working_hours:
                work_hours = working_hours.get_working_hours(
                    from_dt,
                    to_dt,
                    compute_leaves=True,
                    resource_id=employee.resource_id.id)
        return work_hours

    @api.model
    def _get_working_hours(self, employee):
        working_hours = None
        contract = employee.contract_id
        if employee.calendar_id:
            working_hours = employee.calendar_id
        elif contract and contract.working_hours:
            working_hours = contract.working_hours
        return working_hours

    @api.depends('number_of_hours_temp', 'state')
    def _compute_number_of_hours(self):
        for rec in self:
            number_of_hours = rec.number_of_hours_temp
            if rec.type == 'remove':
                number_of_hours = -rec.number_of_hours_temp

            rec.virtual_hours = number_of_hours
            if rec.state not in ('validate',):
                number_of_hours = 0.0
            rec.number_of_hours = number_of_hours

    number_of_hours_temp = fields.Float(
        string='Allocation in Hours',
        digits=(2, 2),
        readonly=True,
        states={'draft': [('readonly', False)],
                'confirm': [('readonly', False)]}
    )
    number_of_hours = fields.Float(
        compute='_compute_number_of_hours',
        store=True
    )
    virtual_hours = fields.Float(
        compute='_compute_number_of_hours',
        store=True
    )
    working_hours = fields.Float(digits=(2, 2))

    @api.one
    @api.constrains(
        'holiday_type',
        'type',
        'employee_id',
        'holiday_status_id')
    def _check_holidays(self):
        if not(self.holiday_type != 'employee' or self.type != 'remove' or
               not self.employee_id or self.holiday_status_id.limit):

            leave_hours = self.holiday_status_id.get_hours(
                self.employee_id
            )
            _logger.debug('Leave Hours: %s', (leave_hours))

            self._check_leave_hours(leave_hours)

    @api.model
    def _check_leave_hours(self, leave_hours):
        remaining = leave_hours['remaining_hours']
        virt_remaining = leave_hours['virtual_remaining_hours']
        if remaining < 0 or virt_remaining < 0:
            # Raising a warning gives a more user-friendly
            # feedback than the default constraint error
            raise ValidationError(_(
                'The number of remaining hours is not sufficient for '
                'this leave type.\nPlease check for allocation requests '
                'awaiting validation.'))

    @api.multi
    def name_get(self):
        res = []
        for leave in self:
            res.append((leave.id, _("%s on %s : %.2f hour(s)") % (
                leave.employee_id.name,
                leave.holiday_status_id.name,
                leave.number_of_hours_temp
            )))
        return res
