# Copyright 2016-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

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
        for status in self.env['hr.holidays.status'].search([]):
            res = status._compute_consumed_allocations()

            for employee_id in res:
                allocations_partial_consumed = res[employee_id]['allocations_partial_consumed']
                allocations_not_consumed = res[employee_id]['allocations_not_consumed']
                allocations_consumed = res[employee_id]['allocations_consumed']

                allocations_partial_consumed._set_notification()
                allocations_partial_consumed._set_expiration()

                allocations_not_consumed._set_notification()
                allocations_not_consumed._set_expiration()

                for allocation in allocations_consumed.filtered(
                        lambda r: r.expiration_date and r.state == 'validate' and not r.expired):
                    allocation.expired = True

    @api.multi
    def _set_notification(self):

        def notification_not_sent(holiday):
            return holiday.email_notify and not holiday.notification_sent

        for holiday in self.filtered(
                lambda r: r.expiration_date and r.state == 'validate' and not r.expired):
            if notification_not_sent(holiday):
                exp_date = datetime.strptime(holiday.expiration_date, DF)
                note_date = datetime.today() + timedelta(holiday.notify_period)

                if exp_date <= note_date and holiday.notify_template_id:
                    recipients = holiday.notify_to.mapped('user_id.partner_id')
                    holiday.notify_template_id.send_mail(
                        holiday.id, email_values={
                            'recipient_ids': [
                                (4, pid) for pid in recipients.ids]})
                    holiday.notification_sent = True

    @api.multi
    def _set_expiration(self):
        for holiday in self.filtered(
                lambda r: r.expiration_date and r.state == 'validate' and not r.expired):
            expiration_date = holiday.expiration_date
            if datetime.strptime(expiration_date, DF) <= datetime.today():
                holiday.expired = True
                if holiday.expire_template_id:
                    recipients = holiday.notify_to.mapped('user_id.partner_id')
                    holiday.expire_template_id.send_mail(
                        holiday.id, email_values={
                            'recipient_ids': [
                                (4, pid) for pid in recipients.ids]})

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
    notify_to = fields.Many2many('hr.employee', string='Notify Expiration to')

    # expiring
    expiration_date = fields.Date()
    expired = fields.Boolean()
    limit = fields.Boolean(related='holiday_status_id.limit')
    expire_template_id = fields.Many2one(
        'mail.template',
        string='Expired Email Template'
    )

    @api.multi
    def _get_duration(self):
        self.ensure_one()
        return self.number_of_days_temp

    @api.multi
    def _set_duration(self, duration):
        self.ensure_one()
        self.number_of_days_temp = duration

    @api.multi
    def _finish_new_allocation(self, new_type):
        for new in self:
            new.holiday_status_id = new_type.id
            if self.env.user.company_id.auto_approve_on_leave_type_archival:
                if new.state == 'draft':
                    new.with_context(tracking_disable=True).action_confirm()
                new.with_context(tracking_disable=True).action_approve()
                if new.state in ['confirm', 'validate1']:
                    new.with_context(tracking_disable=True).action_validate()

    @api.multi
    def _prepare_create_by_category(self, employee):
        values = super(HRHolidays, self)._prepare_create_by_category(employee)
        values.update({
            'email_notify': self.email_notify,
            'notify_period': self.notify_period,
            'notify_template_id': self.notify_template_id.id,
            # 'notify_to': [(6, 0, self.notify_to.ids)],
            'expiration_date': self.expiration_date,
            'expire_template_id': self.expire_template_id.id,
        })
        return values
