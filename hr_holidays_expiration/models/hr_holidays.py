# Copyright 2016-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class HRHolidays(models.Model):
    _inherit = "hr.holidays"

    @api.model
    def default_get(self, fields):
        res = super(HRHolidays, self).default_get(fields)
        company = self.env.user.company_id
        res['expire_template_id'] = (company.expire_template_id.id)
        res['notify_template_id'] = (company.notify_template_id.id)
        return res

    @api.model
    def check_expiring(self):
        allocation_req_list = self.search([
            ('expiration_date', '!=', False),
            ('state', '=', 'validate'),
            ('expired', '=', False),
            ('type', '!=', 'remove')])

        # notification
        allocation_req_list._set_notification()
        # expiring
        allocation_req_list._set_expiration()

    @api.multi
    def _set_notification(self):

        def notification_not_sent(holiday):
            return holiday.email_notify and not holiday.notification_sent

        for holiday in self:
            if notification_not_sent(holiday):
                exp_date = datetime.strptime(holiday.expiration_date, DF)
                note_date = datetime.today() + timedelta(holiday.notify_period)

                if exp_date <= note_date and holiday.notify_template_id:
                    holiday.notify_template_id.send_mail(holiday.id)
                    holiday.notification_sent = True

    @api.multi
    def _set_expiration(self):
        for holiday in self:
            expiration_date = holiday.expiration_date
            if datetime.strptime(expiration_date, DF) <= datetime.today():
                holiday.expired = True
                if holiday.expire_template_id:
                    holiday.expire_template_id.send_mail(holiday.id)

    # notification
    email_notify = fields.Boolean('Notify Expiration via Email')
    notify_period = fields.Integer(
        "Notify period (days)",
        help="The amount of days before the holidays expire to send\
         out the notification email.")
    notify_template_id = fields.Many2one(
        'mail.template',
        string='Notify Email Template'
    )
    notification_sent = fields.Boolean(string='Expiration Notification Sent')
    notify_to = fields.Many2one('hr.employee', string='Notify Expiration to')

    # expiring
    expiration_date = fields.Date()
    expired = fields.Boolean(default=False)
    expire_template_id = fields.Many2one(
        'mail.template',
        string='Expired Email Template'
    )
