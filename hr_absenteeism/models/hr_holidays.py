# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import math
from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTS
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    @api.multi
    def compute_interval(self):
        self.ensure_one()

        date_from = self.date_from
        date_to = datetime.today().strftime(DTS)

        # Compute and update the number of days
        number_of_days_temp = 0
        if date_from <= date_to:
            from_dt = datetime.strptime(date_from, DTS)
            to_dt = datetime.strptime(date_to, DTS)
            timedelta = to_dt - from_dt
            diff_day = timedelta.days + float(timedelta.seconds) / 86400

            number_of_days_temp = round(math.floor(diff_day)) + 1

        self.write({'date_to': date_to,
                    'number_of_days_temp': number_of_days_temp})

    @api.model
    def increase_date_to(self):
        """For running sick days not yet APPROVED increase date_to to today"""
        _logger.debug('ONESTEiN hr_holidays increase_date_to')
        sick_day_ids = self.search(
            [('holiday_status_id.absenteeism_control', '=', True),
             ('state', '=', 'confirm'),
             ('type', '=', 'remove')])

        for sick_day in sick_day_ids:
            date_from = sick_day.date_from
            date_to = datetime.today().strftime(DTS)

            # The following is based on addons/hr_holidays/hr_holidays.py
            # date_to has to be greater than date_from
            if date_from > date_to:
                _logger.warning(
                    'The start date must be anterior to the end date.'
                )
                raise Warning(
                    _('The start date must be anterior to the end date.')
                )
            sick_day.compute_interval()

    def _compute_notify_date(self, notification, holiday):
        notify_date = datetime.strptime(
            holiday.date_from, DTS) + timedelta(
            days=notification.interval)
        return notify_date

    absenteeism_control = fields.Boolean(
        related="holiday_status_id.absenteeism_control",
        string="Absence Control"
    )
    absenteeism_date_ids = fields.One2many(
        "hr.absenteeism.dates",
        "holiday_id",
        "Absenteeism Notification Dates"
    )

    @api.model
    def create(self, vals):
        # Create the related hr_absenteeism_dates
        holiday = super(HrHolidays, self).create(vals)
        if holiday.date_from:
            for notification in holiday.holiday_status_id.notification_ids:
                notify_date = self._compute_notify_date(
                    notification,
                    holiday
                )
                absent_vals = {
                    'name': notification.name,
                    'holiday_id': holiday.id,
                    'absent_notify_date': notify_date,
                    'notification_id': notification.id
                }
                self.env['hr.absenteeism.dates'].create(absent_vals)
        return holiday

    @api.multi
    def _validate_fields(self, field_names):
        # monkey patch hr_holidays constraints
        str = 'You can not have 2 leaves that overlaps on same day!'
        self._constraints = [t for t in self._constraints if t[1] != str]
        return super(HrHolidays, self)._validate_fields(field_names)
