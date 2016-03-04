# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class HrPublicHoliday(models.Model):
    _name = 'hr.public.holiday'

    name = fields.Char('Description', size=64)
    state = fields.Selection(
        [('draft', 'To Approve'),
         ('validate', 'Approved')],
        'Status', readonly=True,
        track_visibility='onchange', copy=False,
        help='The status is set to \'To Submit\', \
              when a holiday request is created.\
              \nThe status is \'Approved\', when holiday request\
              is approved by manager.',
        default='draft')
    date_from = fields.Datetime(
        'Start Date',
        readonly=True,
        states={'draft': [('readonly', False)],
                'confirm': [('readonly', False)]},
        select=True,
        copy=False)
    date_to = fields.Datetime(
        'End Date',
        readonly=True,
        states={'draft': [('readonly', False)],
                'confirm': [('readonly', False)]},
        copy=False)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company')

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
        imd_id, model, res_id = self.env['ir.model.data'].xmlid_lookup(
            'hr_public_holidays.hr_public_holiday')
        for holiday in self:
            _logger.debug("hr_public_holiday reinit: %s" % (self.name,))

            existing = self.env['hr.holidays'].search(
                [('public_holiday_id', '=', holiday.id)])
            new = []
            company = holiday.company_id
            for emp in holiday._employees_for_public_holiday(company):
                matches = [h for h in existing
                           if h.employee_id.id == emp.id and
                           h.public_holiday_id.id == holiday.id]
                if matches:
                    existing = [h for h in existing if h not in matches]
                else:
                    _logger.info(
                        "hr_public_holiday reinit: "
                        "created holiday %s for %s" % (
                         self.name, emp.name))
                    vals = {
                        'name': holiday.name,
                        'type': 'remove',
                        'holiday_type': 'employee',
                        'holiday_status_id': res_id,
                        'date_from': holiday.date_from,
                        'date_to': holiday.date_to,
                        'employee_id': emp.id,
                        'public_holiday_id': holiday.id
                    }
                    new.append(self.env['hr.holidays'].create(vals))

            for leave in existing:
                _logger.info(
                    "hr_public_holiday reinit: "
                    "removed holiday %s for %s" % (
                     self.name, leave.employee_id.name))
                for sig in ('refuse', 'reset'):
                    leave.signal_workflow(sig)
                leave.unlink()

            for leave_id in new:
                for sig in ('confirm', 'validate', 'second_validate'):
                    leave_id.signal_workflow(sig)

    @api.one
    def validate(self):
        self.reinit()
        self.state = 'validate'

    @api.one
    def reset(self):
        self.state = 'draft'
        for holiday in self.env['hr.holidays'].search(
                [('public_holiday_id', '=', self.id)]):
            for sig in ('refuse', 'reset'):
                holiday.signal_workflow(sig)
            holiday.unlink()
