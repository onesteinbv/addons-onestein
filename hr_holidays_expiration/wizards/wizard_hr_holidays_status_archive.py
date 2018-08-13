# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class WizardHrHolidaysStatusArchive(models.TransientModel):
    _name = "wizard.hr.holidays.status.archive"

    holiday_status_id = fields.Many2one(
        'hr.holidays.status',
        string='Next Leave Type',
        required=False
    )

    @api.multi
    def transfer_and_archive_status(self):
        self.ensure_one()

        if not self.holiday_status_id:
            raise ValidationError(_(
                'Please select the Next Leave Type!')
            )

        active_id = self._context.get('active_id')
        old_type = self.env['hr.holidays.status'].browse(active_id)
        res = old_type._compute_consumed_allocations()
        old_type.active = False
        new_type = self.holiday_status_id

        for employee_id in res:
            allocations_partial_consumed = res[employee_id][
                'allocations_partial_consumed']
            amount_partial_consumed = res[employee_id][
                'amount_partial_consumed']
            allocations_not_consumed = res[employee_id][
                'allocations_not_consumed']

            if allocations_partial_consumed:
                new = allocations_partial_consumed.copy()
                new._set_duration(amount_partial_consumed)
                new._finish_new_allocation(new_type)

            for alloc in allocations_not_consumed:
                new = alloc.copy()
                new._set_duration(alloc._get_duration())
                new._finish_new_allocation(new_type)

    @api.multi
    def archive_status(self):
        self.ensure_one()

        active_id = self._context.get('active_id')
        old_type = self.env['hr.holidays.status'].browse(active_id)
        old_type.active = False
