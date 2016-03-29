# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.exceptions import Warning
from openerp.tools.translate import _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def write(self, vals):
        res = super(HrEmployee, self).write(vals)
        if 'company_id' in vals:
            try:
                res_id = self.env['ir.model.data'].get_object(
                    'hr_public_holidays', 'hr_public_holiday').id
            except ValueError:
                raise Warning(
                    _("Leave Type for Public Holiday not found!"))
            for employee in self:
                existing = self.env['hr.holidays'].search(
                    [('employee_id', '=', employee.id),
                     ('public_holiday_id', '!=', False),
                     ('public_holiday_id', '!=', None)])
                for leave in existing:
                    for sig in ('refuse', 'reset'):
                        leave.signal_workflow(sig)
                    self._cr.execute("DELETE FROM hr_holidays WHERE id=%s", (leave.id,))

                new = []
                search_domain = [('state', '=', 'validate'),
                                 '|',
                                 ('company_id', '=', False),
                                 ('company_id', '=', None)]
                if vals['company_id']:
                    search_domain = [('state', '=', 'validate'),
                                     '|', '|',
                                     ('company_id', '=', False),
                                     ('company_id', '=', None),
                                     ('company_id', '=', vals['company_id'])]
                to_create = self.env['hr.public.holiday'].search(
                    search_domain)
                for public_holiday in to_create:
                    dict = {
                        'name': public_holiday.name,
                        'type': 'remove',
                        'holiday_type': 'employee',
                        'holiday_status_id': res_id,
                        'date_from': public_holiday.date_from,
                        'date_to': public_holiday.date_to,
                        'employee_id': employee.id,
                        'public_holiday_id': public_holiday.id
                    }
                    new.append(self.env['hr.holidays'].create(dict))

                for leave_id in new:
                    for sig in ('confirm', 'validate', 'second_validate'):
                        leave_id.signal_workflow(sig)
        return res
