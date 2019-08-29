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
        return super(
            HolidaysRequest,
            self.with_context(o365_override_user=True)
        ).action_refuse()
