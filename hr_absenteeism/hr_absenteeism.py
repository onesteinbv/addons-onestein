# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Onestein (<http://www.onestein.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
import math

from openerp import models, fields, api
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _
from openerp.exceptions import Warning

_logger = logging.getLogger(__name__)


class hr_absenteeism_notifications(models.Model):
    _name = "hr.absenteeism.notifications"
    _description = "Absenteeism Notifications"

    name = fields.Char("Notification Name")
    interval = fields.Integer("Interval (days)")
    leave_type_id = fields.Many2one("hr.holidays.status", string="Leave Type", readonly=True)


class hr_holidays_status(models.Model):
    _inherit = "hr.holidays.status"

    absenteeism_control = fields.Boolean(string="Absence Control")
    notification_ids = fields.One2many("hr.absenteeism.notifications", "leave_type_id", "Notifications")


class hr_absenteeism_dates(models.Model):
    _name = "hr.absenteeism.dates"
    _description = "Absenteeism Notification Dates"

    name = fields.Char("Notification Name")
    absent_notify_date = fields.Datetime("Absent Notification Date")
    holiday_id = fields.Many2one("hr.holidays", string="Related Holiday", ondelete="cascade")
    notification_id = fields.Many2one("hr.absenteeism.notifications", string="Related notification")


class hr_holidays(models.Model):
    _inherit = "hr.holidays"

    @api.cr_uid_ids_context
    def increase_date_to(self, cr, uid, ids, context=None):
        """For running sick days not yet APPROVED increase date_to to today"""
        _logger.debug("ONESTEiN hr_holidays increase_date_to")
        sick_day_ids = self.search(cr, uid, [('holiday_status_id.absenteeism_control', '=', True),
                                             ('state', '=', 'confirm'),
                                             ('type', '=', 'remove')])

        for sick_day_id in sick_day_ids:
            sick_day = self.browse(cr, uid, sick_day_id, context=context)
            date_from = sick_day.date_from
            date_to = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            if date_from:
                # The following is based on addons/hr_holidays/hr_holidays.py
                # date_to has to be greater than date_from
                if (date_from and date_to) and (date_from > date_to):
                    _logger.warning("The start date must be anterior to the end date.")
                    raise Warning(_('Warning!'),_('The start date must be anterior to the end date.'))

                # Compute and update the number of days
                if (date_to and date_from) and (date_from <= date_to):
                    from_dt = datetime.strptime(date_from, DEFAULT_SERVER_DATETIME_FORMAT)
                    to_dt = datetime.strptime(date_to, DEFAULT_SERVER_DATETIME_FORMAT)
                    timedelta = to_dt - from_dt
                    diff_day = timedelta.days + float(timedelta.seconds) / 86400

                    number_of_days_temp = round(math.floor(diff_day))+1
                else:
                    number_of_days_temp = 0

                self.write(cr, uid, sick_day_id, {'date_to': date_to, 'number_of_days_temp': number_of_days_temp}, context=context)
            else:
                _logger.warning("ONESTEiN hr_holidays increase_date_to no date_from set")
        return True

    def _compute_notify_date(self, notification, holiday):
        notify_date = datetime.strptime(holiday.date_from, DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(
            days=notification.interval)
        return notify_date

    def create(self, cr, uid, vals, context=None):
        # Create the related hr_absenteeism_dates
        res = super(hr_holidays, self).create(cr, uid, vals, context)
        holiday = self.browse(cr, uid, res, context)
        for notification in holiday.holiday_status_id.notification_ids:
            if holiday.date_from:
                notify_date = self._compute_notify_date(notification, holiday)
                absent_vals = {
                    "name": notification.name, "holiday_id": res, "absent_notify_date": notify_date,
                    "notification_id": notification.id
                }
                self.pool.get("hr.absenteeism.dates").create(cr, uid, absent_vals, context)
        return res

    @api.multi
    def _validate_fields(self, field_names):
        ### monkey patch hr_holidays constraints
        self._constraints = [t for t in self._constraints if t[1] != 'You can not have 2 leaves that overlaps on same day!']
        return super(hr_holidays, self)._validate_fields(field_names)
