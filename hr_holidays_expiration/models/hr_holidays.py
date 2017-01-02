# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from datetime import datetime, timedelta

from openerp import api, fields, models
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

_logger = logging.getLogger(__name__)


class hr_holidays(models.Model):
    _inherit = "hr.holidays"

    @api.multi
    def holidays_validate(self):
        self.approval_date = datetime.today()
        res = super(hr_holidays, self).holidays_validate()
        return res

    @api.cr_uid_ids_context
    def send_notifications(
            self, cr, uid, ids, holiday_id, tmpl_id=False, context=None):
        if holiday_id and tmpl_id:
            _logger.debug("ONESTEiN hr_holidays send_notifications")
            mtp = self.pool.get('mail.template')
            mtp.send_mail(cr, uid, tmpl_id, holiday_id, context=context)
        return {}

    @api.model
    def check_expiring(self):
        _logger.debug("ONESTEiN hr_holidays check_expiring")
        allocation_req_list = self.search([
            ('expiration_date', '!=', False),
            ('approval_date', '!=', False),
            ('expired', '=', False),
            ('type', '!=', 'remove')])
        for holiday in allocation_req_list:
            today = datetime.today()
            email_notify = holiday.email_notify
            notification_sent = holiday.notification_sent
            # notification
            if email_notify and not notification_sent and datetime.strptime(
                    holiday.expiration_date, DF) <= today + timedelta(
                        holiday.notify_period):
                holiday.send_notifications(
                    holiday_id=holiday.id,
                    tmpl_id=holiday.notify_template_id.id
                )
                holiday.notification_sent = True
            # expiring
            if datetime.strptime(
                    holiday.expiration_date, DF) <= today:
                holiday.expired = True
                holiday.send_notifications(
                    holiday_id=holiday.id,
                    tmpl_id=holiday.expire_template_id.id
                )

    # notification
    email_notify = fields.Boolean(
        "Notify Expiration via Email", default=False)
    notify_period = fields.Integer(
        "Notify period (days)",
        help="The amount of days before the holidays expire to send\
         out the notification email.")
    notify_template_id = fields.Many2one(
        'mail.template',
        string="Notify Email Template",
        default=lambda self: self.env.user.company_id.notify_template_id)
    notification_sent = fields.Boolean(
        string="Expiration Notification Sent")
    notify_to = fields.Many2one(
        'hr.employee', string="Notify Expiration to")

    # expiring
    expiration_date = fields.Date(string='Expiration Date')
    expired = fields.Boolean(string="Expired", default=False)
    expire_template_id = fields.Many2one(
        'mail.template', string="Expired Email Template",
        default=lambda self: self.env.user.company_id.expire_template_id)
    approval_date = fields.Date(string="Date Approved")
