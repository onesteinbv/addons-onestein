# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    public_holiday_id = fields.Many2one(
        'hr.public.holiday',
        string="Public Holiday")

    @api.model
    def get_employee_calendar(self, employee):
        calendar = None
        if employee.resource_id.calendar_id:
            calendar = employee.resource_id.calendar_id.id
        return calendar

    @api.one
    def holidays_validate(self):
        if not self.holiday_type == 'employee':
            return super(HrHolidays, self).holidays_validate()

        try:
            imd_id, model, res_id = self.env['ir.model.data'].xmlid_lookup(
                'hr_public_holidays.hr_public_holiday')
        except ValueError:
            return super(HrHolidays, self).holidays_validate()

        if self.holiday_status_id.id != res_id:
            return super(HrHolidays, self).holidays_validate()

        calendar = self.get_employee_calendar(self.employee_id)

        self.env['resource.calendar.leaves'].create({
            'name': self.name,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'resource_id': self.employee_id.resource_id.id,
            'calendar_id': calendar,
            'holiday_id': self.id
        })
        self.state = 'validate'
