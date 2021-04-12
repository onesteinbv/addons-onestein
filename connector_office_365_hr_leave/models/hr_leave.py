# Copyright 2019-2021 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import api, fields, models
from odoo.addons.connector_office_365 import Office365Error

_logger = logging.getLogger(__name__)


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
        self.sudo().need_o365_manual_push = False
        self._office_365_push()

    def _office_365_activity_require_auth(self):
        # create activity to ask user to authenticate
        xmlid = (
            'connector_office_365_hr_leave.'
            'mail_act_office_365_authenticate'
        )
        self.sudo().activity_schedule(xmlid, user_id=self.user_id.id)

    def _office_365_push(self):
        user = self.meeting_id.user_id
        if user.office_365_access_token and user.office_365_expiration > fields.Datetime.now():
            try:
                self.meeting_id.sudo(user).with_context(
                    origin_leave_id=self.id
                ).office_365_push()
            except Office365Error as exc:
                _logger.warning(
                    'Error pushing meeting %d of leave %d: %s',
                    self.meeting_id.id, self.id, exc
                )
                self.sudo().need_o365_manual_push = True
        else:
            self.sudo().need_o365_manual_push = True
        if self.need_o365_manual_push:
            self._office_365_activity_require_auth()

    def _validate_leave_request(self):
        super()._validate_leave_request()
        for leave in self:
            if not leave.meeting_id and leave.meeting_id.user_id:
                continue
            leave._office_365_push()

    @api.multi
    def action_refuse(self):
        res = False
        activity_scheduled = set()
        now = fields.Datetime.now()
        leaves_non_expired_tokens = self.filtered(
            lambda r: r.meeting_id.user_id.office_365_access_token and
            r.meeting_id.office_365_expiration > now
        )
        leaves_expired_tokens = self - leaves_non_expired_tokens
        for rec in leaves_non_expired_tokens:
            try:
                res = super(
                    HolidaysRequest,
                    rec.with_context(o365_override_user=True)
                ).action_refuse()
            except Office365Error:
                leaves_expired_tokens += rec
        for rec in leaves_expired_tokens:
            # don't delete event from office365, create an activity
            # requesting the user to auth on office (at most 1 activity per user)
            res = super(
                HolidaysRequest,
                rec.with_context(office_365_force=True)
            ).action_refuse()
            # don't flood the user with activities
            if rec.user_id not in activity_scheduled:
                rec._office_365_activity_require_auth()
                activity_scheduled.add(rec.user_id)
        return res
