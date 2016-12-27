# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError, Warning
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class hr_holidays(models.Model):
    _inherit = "hr.holidays"

    @api.multi
    @api.onchange('employee_id')
    def onchange_holiday_employee(self):
        for holiday in self:
            holiday.department_id = None
            holiday.number_of_hours_temp = 0.0
            if holiday.employee_id:
                employee = holiday.employee_id
                holiday.number_of_hours_temp = 0.0
                from_dt = False
                to_dt = False
                user = self.env.user
                working_hours = None
                if employee.calendar_id:
                    working_hours = employee.calendar_id
                elif employee.contract_id:
                    if employee.contract_id.working_hours:
                        working_hours = employee.contract_id.working_hours
                if working_hours:
                    if holiday.date_from:
                        from_dt = fields.Datetime.from_string(
                            holiday.date_from
                        )
                        from_dt = fields.Datetime.context_timestamp(
                            user, from_dt
                        )
                        from_dt = from_dt.replace(tzinfo=None)
                    if holiday.date_to:
                        to_dt = fields.Datetime.from_string(
                            holiday.date_to
                        )
                        to_dt = fields.Datetime.context_timestamp(
                            user, to_dt
                        )
                        to_dt = to_dt.replace(tzinfo=None)
                    if from_dt and to_dt:
                        work_hours = working_hours.get_working_hours(
                            start_dt=from_dt,
                            end_dt=to_dt,
                            compute_leaves=True,
                            resource_id=employee.resource_id.id
                        )
                        holiday.number_of_hours_temp = work_hours
                        holiday.department_id = employee.department_id

    @api.multi
    @api.onchange('date_from', 'date_to')
    def onchange_date(self):
        for holiday in self:
            from_dt = False
            to_dt = False
            work_hours = 0.0
            user = self.env.user
            employee = holiday.employee_id
            # Check in context what form is open: add or remove
            if self.env.context.get('default_type', '') == 'add':
                return

            if holiday.date_from:
                from_dt = fields.Datetime.from_string(holiday.date_from)
                from_dt = fields.Datetime.context_timestamp(user, from_dt)
                from_dt = from_dt.replace(tzinfo=None)
            if holiday.date_to:
                to_dt = fields.Datetime.from_string(holiday.date_to)
                to_dt = fields.Datetime.context_timestamp(user, to_dt)
                to_dt = to_dt.replace(tzinfo=None)

            # date_to has to be greater than date_from
            if holiday.date_from and holiday.date_to and (from_dt > to_dt):
                raise Warning(_(
                    'The start date must be anterior to the end date.'
                ))

            if not employee and (holiday.date_to or holiday.date_from):
                raise Warning(_('Set an employee first!'))

            if from_dt and to_dt:
                working_hours = None
                contract = employee.contract_id
                if employee.calendar_id:
                    working_hours = employee.calendar_id
                elif contract and contract.working_hours:
                    working_hours = contract.working_hours
                if working_hours:
                    work_hours = working_hours.get_working_hours(
                        from_dt,
                        to_dt,
                        compute_leaves=True,
                        resource_id=employee.resource_id.id)

            holiday.number_of_hours_temp = work_hours

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
        string='Number of Hours',
        compute='_compute_number_of_hours',
        store=True
    )
    virtual_hours = fields.Float(
        string='Virtual Hours',
        compute='_compute_number_of_hours',
        store=True
    )
    working_hours = fields.Float(
        string='Working hours', digits=(2, 2)
    )

    @api.one
    @api.constrains(
        'holiday_type',
        'type',
        'employee_id',
        'holiday_status_id',
        'holiday_status_id')
    def _check_holidays(self):
        if not(self.holiday_type != 'employee' or self.type != 'remove' or
               not self.employee_id or self.holiday_status_id.limit):

            leave_hours = self.holiday_status_id.get_hours(
                self.employee_id.id
            )
            _logger.debug('Leave Hours: %s', (leave_hours))

            if (leave_hours['remaining_hours'] < 0 or
                    leave_hours['virtual_remaining_hours'] < 0):
                # Raising a warning gives a more user-friendly
                # feedback than the default constraint error
                raise ValidationError(_(
                    'The number of remaining hours is not sufficient for '
                    'this leave type.\nPlease check for allocation requests '
                    'awaiting validation.'))

    ####################################################
    # ORM Overrides methods
    ####################################################

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
