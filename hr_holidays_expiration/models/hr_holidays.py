# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

_logger = logging.getLogger(__name__)


class hr_holidays(models.Model):
    _inherit = "hr.holidays"

    @api.multi
    def holidays_validate(self):
        self.approval_date = datetime.today()
        res = super(hr_holidays, self).holidays_validate()
        return res

    @api.model
    def check_expiring(self):
        _logger.debug("ONESTEiN hr_holidays check_expiring")
        allocation_req_list = self.search([
            ('expiration_date', '!=', False),
            ('approval_date', '!=', False),
            ('expired', '=', False),
            ('type', '!=', 'remove')])
        for holiday in allocation_req_list:
            # notification
            if holiday.email_notify and not holiday.notification_sent and datetime.strptime(
                    holiday.expiration_date,
                    DEFAULT_SERVER_DATE_FORMAT) <= datetime.today() + timedelta(
                        holiday.notify_period):
                if holiday.notify_template_id:
                    holiday.notify_template_id.send_mail(holiday.id)
                    holiday.notification_sent = True
            # expiring
            if datetime.strptime(
                    holiday.expiration_date,
                    DEFAULT_SERVER_DATE_FORMAT) <= datetime.today():
                holiday.expired = True
                if holiday.expire_template_id:
                    holiday.expire_template_id.send_mail(holiday.id)

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
