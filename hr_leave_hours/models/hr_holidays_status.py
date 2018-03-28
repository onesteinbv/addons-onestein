# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class hr_holidays_status(models.Model):
    _inherit = "hr.holidays.status"

    def get_hours_domain(self, cr, uid, domain=[], context=None):
        """
        Hook to change the return domain
        :return: domain
        """
        return domain

    @api.cr_uid_ids_context
    def get_hours(self, cr, uid, ids, employee_id, context=None):
        result = dict((id, dict(max_hours=0, hours_taken=0, remaining_hours=0,
                                virtual_remaining_hours=0)) for id in ids)
        hours_domain = [('employee_id', '=', employee_id),
                        ('state', 'in', ['confirm', 'validate1', 'validate']),
                        ('holiday_status_id', 'in', ids)
                        ]
        hours_domain = self.get_hours_domain(cr, uid, hours_domain, context=context)
        holiday_ids = self.pool['hr.holidays'].search(cr, uid, hours_domain, context=context)

        for holiday in self.pool['hr.holidays'].browse(cr, uid, holiday_ids, context=context):
            status_dict = result[holiday.holiday_status_id.id]
            if holiday.type == 'add':
                status_dict['virtual_remaining_hours'] += holiday.number_of_hours_temp
                if holiday.state == 'validate':
                    status_dict['max_hours'] += holiday.number_of_hours_temp
                    status_dict['remaining_hours'] += holiday.number_of_hours_temp
            elif holiday.type == 'remove':  # number of days is negative
                status_dict['virtual_remaining_hours'] -= holiday.number_of_hours_temp
                if holiday.state == 'validate':
                    status_dict['hours_taken'] += holiday.number_of_hours_temp
                    status_dict['remaining_hours'] -= holiday.number_of_hours_temp
        return result

    @api.cr_uid_ids_context
    def _user_left_hours(self, cr, uid, ids, context=None):
        employee_id = False
        if context and 'employee_id' in context:
            employee_id = context['employee_id']
        else:
            employee_ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
            if employee_ids:
                employee_id = employee_ids[0]
        if employee_id:

            res = self.get_hours(cr, uid, ids, employee_id, context=context)

        else:
            res = dict((res_id, {'hours_taken': 0, 'virtual_remaining_hours': 0, 'remaining_hours': 0, 'max_hours': 0}) for res_id in ids)
        return res

    max_hours = fields.Float(compute="_user_left_hours",
                              string='Maximum Allowed Hours')
    hours_taken = fields.Float(compute="_user_left_hours",
                                string='Hours Already Taken')
    remaining_hours = fields.Float(compute="_user_left_hours",
                                   string='Remaining Hours')
    virtual_remaining_hours = fields.Float(compute="_user_left_hours",
                                           string='Virtual Remaining Hours')

    @api.cr_uid_ids_context
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not context.get('employee_id',False):
            # leave counts is based on employee_id, would be inaccurate if not based on correct employee
            return super(hr_holidays_status, self).name_get(cr, uid, ids, context=context)

        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            if not record.limit:
                hours_employee = self._user_left_hours(cr, uid, ids, context=context)
                hours_left = hours_employee.get(record.id)
                name = name + ('  (%.1f Left)' % (hours_left.get('max_hours',0.0)-hours_left.get('hours_taken',0.0)))
            res.append((record.id, name))
        return res
