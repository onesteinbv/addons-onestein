# Copyright 2019 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    need_o365_authenticate = fields.Boolean(
        compute="_compute_need_o365_authenticate",
    )
    need_o365_manual_push = fields.Boolean()

    @api.depends('meeting_id.user_id.office_365_access_token')
    def _compute_need_o365_authenticate(self):
        for leave in self:
            leave.need_o365_authenticate = (
                self.meeting_id.user_id and
                self.env.user == self.meeting_id.user_id and
                not self.env.user.office_365_access_token
            )

    def office_365_authenticate(self):
        return self.meeting_id.user_id.button_office_365_authenticate()

    def office_365_manual_push(self):
        self.ensure_one()
        self._office_365_push()
        self.need_o365_manual_push = False

    def _office_365_push(self):
        user = self.meeting_id.user_id
        if user.office_365_access_token:
            self.meeting_id.sudo(user).with_context(
                origin_leave_id=self.id
            ).office_365_push()
        else:
            self.need_o365_manual_push = True
            # create activity to ask user to authenticate
            xmlid = (
                'connector_office_365_hr_leave.'
                'mail_act_office_365_authenticate'
            )
            self.activity_schedule(xmlid, user_id=self.user_id.id)

    def _validate_leave_request(self):
        super()._validate_leave_request()
        for leave in self:
            if not leave.meeting_id and leave.meeting_id.user_id:
                continue
            leave._office_365_push()

    @api.multi
    def action_refuse(self):
        # Copied from odoo
        # not sure about the copy but _remove_resource_leave searches through
        # all leaves might be an issue with lots of data
        current_employee = self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)],
            limit=1
        )
        for holiday in self:
            if holiday.state not in ['confirm', 'validate', 'validate1']:
                raise UserError(_(
                    'Leave request must be confirmed or validated '
                    'in order to refuse it.'))

            if holiday.state == 'validate1':
                holiday.write({
                    'state': 'refuse',
                    'first_approver_id': current_employee.id
                })
            else:
                holiday.write({
                    'state': 'refuse',
                    'second_approver_id': current_employee.id
                })
            # Delete the meeting
            if holiday.meeting_id:
                # Change from odoo pass meeting creator as user
                holiday.meeting_id.with_context(
                    user=holiday.meeting_id.user_id
                ).unlink()

            # If a category that created several holidays, cancel all related
            holiday.linked_request_ids.action_refuse()
        self._remove_resource_leave()
        self.activity_update()
        return True
