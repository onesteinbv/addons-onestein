# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class HrHolidaysStatus(models.Model):
    _inherit = "hr.holidays.status"

    holiday_ids = fields.One2many(
        'hr.holidays',
        'holiday_status_id',
        string='Holidays'
    )

    @api.model
    def _check_init_dict(self, employee_id, res):
        if employee_id not in res:
            res[employee_id] = {
                'consumed_leaves': 0.0,
                'amount_counter': 0.0,
                'amount_partial_consumed': 0.0,
                'allocations_partial_consumed': self.env['hr.holidays'],
                'allocations_not_consumed': self.env['hr.holidays'],
                'allocations_consumed': self.env['hr.holidays'],
            }

    @api.multi
    def _set_consumed_leaves(self, res):
        self.ensure_one()
        for leave in self.holiday_ids.filtered(
            lambda r: r.type == 'remove' and r.state in [
                'confirm', 'validate1', 'validate']):
            employee_id = leave.employee_id.id
            self._check_init_dict(employee_id, res)
            consumed_leaves = leave._get_duration()
            res[employee_id]['consumed_leaves'] += consumed_leaves

    @api.multi
    def _set_consumed_allocations(self, res):
        self.ensure_one()
        for allocation in self.holiday_ids.filtered(
            lambda r: r.type == 'add' and
                r.state in ['confirm', 'validate1', 'validate']
        ).sorted(key=lambda r: r.expiration_date or ''):
            self._set_data_from_consumed_allocation(allocation, res)

    @api.model
    def _set_data_from_consumed_allocation(self, allocation, res):
        employee_id = allocation.employee_id.id
        allocated_amount = allocation._get_duration()
        self._check_init_dict(employee_id, res)
        if res[employee_id]['amount_counter'] + allocated_amount > \
                res[employee_id]['consumed_leaves']:
            if res[employee_id]['amount_counter'] < res[employee_id]['consumed_leaves']:
                amount_partial_consumed = res[employee_id]['amount_counter'] + \
                    allocated_amount - res[employee_id]['consumed_leaves']
                res[employee_id]['amount_partial_consumed'] = amount_partial_consumed
                res[employee_id]['allocations_partial_consumed'] += allocation
            else:
                res[employee_id]['allocations_not_consumed'] += allocation
        else:
            res[employee_id]['allocations_consumed'] += allocation
        res[employee_id]['amount_counter'] += allocated_amount

    @api.multi
    def _compute_consumed_allocations(self):
        self.ensure_one()
        res = {}
        self._set_consumed_leaves(res)
        self._set_consumed_allocations(res)
        return res

    @api.multi
    def toggle_active(self):
        for record in self:
            if record.active and not record.limit:
                view = self.env.ref(
                    'hr_holidays_expiration.wizard_hr_holidays_status_archive'
                )

                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Close Holidays Status'),
                    'view_mode': 'form',
                    'res_model': 'wizard.hr.holidays.status.archive',
                    'target': 'new',
                    'views': [[view.id, 'form']],
                }

        return super(HrHolidaysStatus, self).toggle_active()
