# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openerp import models, api
from openerp.exceptions import Warning
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class HrHolidaysPublicLine(models.Model):
    _inherit = 'hr.holidays.public.line'

    @api.model
    def _employees_for_public_holiday(self, company):
        company_id = company and company.id or None
        employees = self.env['hr.employee'].search(
            ['|',
             ('company_id', '=', company_id),
             ('company_id', '=', False)])
        return employees

    @api.multi
    def reinit(self):
        try:
            res_id = self.env['ir.model.data'].get_object(
                'hr_public_holidays_leaves', 'hr_public_holiday').id
        except ValueError:
            raise Warning(
                _("Leave Type for Public Holiday not found!"))
        for holiday_line in self:
            existing = self.env['hr.holidays'].search(
                [('public_holiday_id', '=', holiday_line.id)])
            new = []
            company = holiday_line.year_id.company_id
            employees = holiday_line._employees_for_public_holiday(company)
            for emp in employees:

                    matches = [h for h in existing
                               if h.employee_id.id == emp.id and
                               h.public_holiday_id.id == holiday_line.id]
                    if matches:
                        existing = [h for h in existing if h not in matches]
                    else:

                        vals = {
                            'name': holiday_line.name,
                            'type': 'remove',
                            'holiday_type': 'employee',
                            'holiday_status_id': res_id,
                            'date_from': holiday_line.date,
                            'date_to': holiday_line.date,
                            'employee_id': emp.id,
                            'public_holiday_id': holiday_line.id
                        }
                        new.append(self.env['hr.holidays'].create(vals))

            for leave in existing:
                _logger.info(
                    "line reinit: "
                    "removed holiday %s for %s" %
                    (leave.name, leave.employee_id.name)
                )
                for sig in ('refuse', 'reset'):
                    leave.signal_workflow(sig)
                leave.unlink()

            for leave_id in new:
                for sig in ('confirm', 'validate', 'second_validate'):
                    leave_id.signal_workflow(sig)

    @api.multi
    def reset(self):
        for line in self:
            for holiday in self.env['hr.holidays'].search(
                    [('public_holiday_id', '=', line.id)]):
                for sig in ('refuse', 'reset'):
                    holiday.signal_workflow(sig)
                holiday.unlink()
