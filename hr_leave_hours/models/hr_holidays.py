# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
from openerp import models, fields, api
from openerp.tools.translate import _


class hr_holidays(models.Model):
    _inherit = "hr.holidays"

    def write(self, cr, uid, ids, vals, context=None):
        if type(ids) == int:
            ids = [ids]
        res = {}
        for holiday in self.browse(cr, uid, ids, context=context):
            if "number_of_hours_temp" not in vals:
                if "date_from" in vals:
                    new = self.onchange_date_from(
                        cr, uid, ids, vals.get("employee_id", holiday.employee_id.id),
                        vals.get("date_to", holiday.date_to), vals["date_from"], context=context)
                    vals.update(new["value"])
                if "date_to" in vals:
                    new = self.onchange_date_to(
                        cr, uid, ids, vals.get("employee_id", holiday.employee_id.id),
                        vals["date_to"], vals.get("date_from", holiday.date_from), context=context)
                    vals.update(new["value"])
                if "employee_id" in vals:
                    new = self.onchange_employee(
                        cr, uid, ids, vals["employee_id"], vals.get("date_to", holiday.date_to),
                        vals.get("date_from", holiday.date_from), context=context)
                    vals.update(new["value"])
            res = super(hr_holidays, self).write(cr, uid, ids, vals, context=context)
        return res

    @api.cr_uid_ids_context
    def onchange_employee(self, cr, uid, ids, employee_id, date_to, date_from, work_hours=0.0, context=None):
        result = self.onchange_date(cr, uid, ids, employee_id, date_to, date_from, work_hours, context)
        if employee_id:
            employee = self.pool.get('hr.employee').browse(cr, uid, employee_id)
            department_id = (employee.department_id and employee.department_id.id) or False
            result['value'].update({'department_id': department_id})
        return result

    @api.cr_uid_ids_context
    def onchange_date(self, cr, uid, ids, employee_id, date_to, date_from, hours=0.0, context=None):
        result = {'value': {}}
        from_dt = False
        to_dt = False
        work_hours = 0.0
        employee = False
        user = self.pool.get('res.users').browse(cr, uid, [uid],context=context)
        # Check in context what form is open: add or remove
        if context and context.get('default_type') == 'add':
            return result

        if employee_id:
            employee = self.pool.get('hr.employee').browse(
                cr, uid, employee_id, context=context)

        if date_from:
            from_dt = fields.Datetime.from_string(date_from)
            from_dt = fields.Datetime.context_timestamp(user, from_dt)
            from_dt = from_dt.replace(tzinfo=None)
            date_from = fields.Datetime.to_string(from_dt)
        if date_to and date_from:
            to_dt = fields.Datetime.from_string(date_to)
            to_dt = fields.Datetime.context_timestamp(user, to_dt)
            to_dt = to_dt.replace(tzinfo=None)
            date_to = fields.Datetime.to_string(to_dt)
        elif date_from:
            to_dt = from_dt.replace(tzinfo=None)
            to_dt = fields.Datetime.context_timestamp(user, to_dt)
            to_dt = to_dt.replace(tzinfo=None)
            date_to = fields.Datetime.to_string(to_dt)

        if from_dt and to_dt and employee:
            if employee.contract_id and employee.contract_id.working_hours:
                work_hours = self.pool.get('resource.calendar').\
                    get_working_hours(
                    cr, uid, employee.contract_id.working_hours.id,
                    from_dt, to_dt, compute_leaves=True,
                    resource_id=employee.resource_id.id, context=context)

        result['value']['number_of_hours_temp'] = work_hours

        # date_to has to be greater than date_from
        if (date_from and date_to) and (from_dt > to_dt):
            raise models.api.Warning(_('Warning'),_('The start date must be anterior to the end date.'))

        # hours needs to be smaller or equal to work_hours
        #if hours and work_hours and hours > work_hours:
        #    raise models.api.Warning(_('Warning'),_('You are trying to allocate more hours then in work schedule'))

        return result

    @api.cr_uid_ids_context
    def onchange_date_to(self, cr, uid, ids, employee_id, date_to, date_from, hours=0.0, context=None):
        if context.get('change_number_of_hours_temp'):
            return
        result = super(hr_holidays, self).onchange_date_to(cr, uid, ids, date_to, date_from)
        new_result = self.onchange_date(cr, uid, ids, employee_id, date_to, date_from, hours, context=context)
        if result['value'] and result['value']['number_of_days_temp']:
            new_result['value']['number_of_days_temp'] = result['value']['number_of_days_temp']
        return new_result

    @api.cr_uid_ids_context
    def onchange_date_from(self, cr, uid, ids, employee_id, date_to, date_from, hours=0.0, context=None):
        result = super(hr_holidays, self).onchange_date_from(cr, uid, ids, date_to, date_from)
        new_result = self.onchange_date(cr, uid, ids, employee_id, date_to, date_from, hours, context=context)
        if result['value'] and result['value']['number_of_days_temp']:
            new_result['value']['number_of_days_temp'] = result['value']['number_of_days_temp']
        return new_result

    def _date_from_hours(self, hours, date_from, date_to, employee):
        user = self.env.user
        delta_utcoffset = None
        from_dt = fields.Datetime.from_string(date_from)
        from_dt_orig = from_dt.replace(tzinfo=None)
        from_dt = fields.Datetime.context_timestamp(user, from_dt)
        from_dt_utcoffset = from_dt.tzinfo._utcoffset
        from_dt = from_dt.replace(tzinfo=None)
        diff = from_dt - from_dt_orig
        to_dt = None
        if date_to and date_from:
            to_dt = fields.Datetime.from_string(date_to)
            to_dt = fields.Datetime.context_timestamp(user, to_dt)
            to_dt_utcoffset = to_dt.tzinfo._utcoffset
            delta_utcoffset = (from_dt_utcoffset - to_dt_utcoffset)
            to_dt = to_dt.replace(tzinfo=None)
        if delta_utcoffset:
            to_dt += delta_utcoffset
        work_hours = self.pool.get('resource.calendar'). \
            get_working_hours(self._cr,
                              self._uid,
                              employee.contract_id.working_hours.id,
                              from_dt,
                              to_dt,
                              compute_leaves=True,
                              resource_id=employee.resource_id.id,
                              context=self._context
                              )
        hours_diff = hours - work_hours
        while abs(hours_diff) > 0.01 and work_hours:
            if hours_diff > 0:
                to_dt += timedelta(hours=abs(hours_diff))
            else:
                to_dt -= timedelta(hours=abs(hours_diff))
            to_dt_string = fields.Datetime.to_string(to_dt)
            to_dt_new = fields.Datetime.from_string(to_dt_string)
            to_dt_new = fields.Datetime.context_timestamp(user, to_dt_new)
            to_dt_utcoffset = to_dt_new.tzinfo._utcoffset
            delta_utcoffset = (from_dt_utcoffset - to_dt_utcoffset)
            work_hours = self.pool.get('resource.calendar'). \
                get_working_hours(self._cr,
                                  self._uid,
                                  employee.contract_id.working_hours.id,
                                  from_dt,
                                  to_dt,
                                  compute_leaves=True,
                                  resource_id=employee.resource_id.id,
                                  context=self._context
                                  )
            hours_diff = hours - work_hours
        return fields.Datetime.to_string(to_dt - diff + delta_utcoffset)

    def _get_date_from_hours_noobj(self, number_of_hours_temp, date_from, date_to, employee_id):
        if number_of_hours_temp and date_from and employee_id:
            employee = self.env['hr.employee'].browse(employee_id)
            if employee.contract_id and employee.contract_id.working_hours:
                hours = number_of_hours_temp
                date_from = date_from
                date_to = date_to
                return self._date_from_hours(hours, date_from, date_to, employee)
        return None

    def _get_date_from_hours(self, holiday):
        if holiday and holiday.number_of_hours_temp and holiday.date_from and holiday.employee_id:
            employee = holiday.employee_id
            if employee.contract_id and employee.contract_id.working_hours:
                hours = holiday.number_of_hours_temp
                date_from = holiday.date_from
                date_to = holiday.date_to
                return self._date_from_hours(hours, date_from, date_to, employee)
        return None

    @api.multi
    @api.onchange('number_of_hours_temp')
    def onchange_number_of_hours_temp(self):
        if not self._context.get('change_number_of_hours_temp'):
            return
        for holiday in self:
            duration = self._get_date_from_hours(holiday)
            if duration:
                holiday.date_to = duration
        return

    @api.depends('number_of_hours_temp','state')
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
        string='Allocation in Hours', digits=(2, 2), readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    number_of_hours = fields.Float(
        string='Number of Hours', compute="_compute_number_of_hours", store=True)
    virtual_hours = fields.Float(
        string='Virtual Hours', compute="_compute_number_of_hours", store=True)
    working_hours = fields.Float(
        string='Working hours', digits=(2, 2))

    def _check_date(self, cr, uid, ids, context=None):
        #THIS METHOD OVERRIDES THE METHOD _check_date DEFINED ON THE MODULE hr_holidays, BASICALLY REMOVING A CONSTRAINT
        return True

    _check_holidays = lambda self, cr, uid, ids, context=None: self.check_holidays(cr, uid, ids, context=context)

    def check_holidays(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            if record.holiday_type != 'employee' or record.type != 'remove' or not record.employee_id or record.holiday_status_id.limit:
                continue
            leave_hours = self.pool.get('hr.holidays.status').get_hours(cr, uid, [record.holiday_status_id.id], record.employee_id.id, context=context)[record.holiday_status_id.id]
            if leave_hours['remaining_hours'] < 0 or leave_hours['virtual_remaining_hours'] < 0:
                # Raising a warning gives a more user-friendly feedback than the default constraint error
                raise Warning(_('The number of remaining hours is not sufficient for this leave type.\n'
                                'Please verify also the leaves waiting for validation.'))
        return True

    _constraints = [
        (_check_date, 'You can not try to allocate more hours then allowed by your working schedule', ['date_from','date_to','state','number_of_hours_temp']),
        (_check_holidays, 'The number of remaining hours is not sufficient for this leave type', ['state','number_of_hours_temp'])
    ]
