# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime

from odoo import api, models


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    @api.model
    def _get_work_limits(self, end_dt, start_dt):
        # Computes start_dt, end_dt (with default values if not set)
        # + off-interval work limits
        work_limits = []
        if start_dt is None and end_dt is not None:
            start_dt = end_dt.replace(
                hour=0, minute=0, second=0)
        elif start_dt is None:
            start_dt = datetime.datetime.now().replace(
                hour=0, minute=0, second=0)
        else:
            work_limits.append((start_dt.replace(
                hour=0, minute=0, second=0), start_dt))
        if end_dt is None:
            end_dt = start_dt.replace(
                hour=23, minute=59, second=59)
        else:
            work_limits.append((end_dt, end_dt.replace(
                hour=23, minute=59, second=59)))
        assert start_dt.date() == end_dt.date(), \
            'get_working_intervals_of_day is restricted to one day'
        return start_dt, work_limits

    @api.multi
    def _get_intervals(self, start_dt, work_dt, work_limits):
        work_intervals = []
        for calendar_work_day in self.get_attendances_for_weekday(start_dt):
            work_day_hour_from = calendar_work_day.hour_from
            work_day_hour_to = calendar_work_day.hour_to
            working_interval = (
                work_dt.replace(
                    hour=int(work_day_hour_from),
                    minute=int(
                        (work_day_hour_from - int(work_day_hour_from)) * 60
                    )),
                work_dt.replace(
                    hour=int(work_day_hour_to),
                    minute=int(
                        (work_day_hour_to - int(work_day_hour_to)) * 60
                    ))
            )
            work_intervals += self.interval_remove_leaves(
                working_interval,
                work_limits
            )

        return work_intervals

    @api.multi
    def get_working_intervals_of_day(
            self, start_dt=None, end_dt=None,
            leaves=None, compute_leaves=False, resource_id=None,
            default_interval=None):
        """ Override method because of the working intervals not
        calculating the minutes only the hours"""

        start_dt, work_limits = self._get_work_limits(end_dt, start_dt)

        intervals = []
        work_dt = start_dt.replace(hour=0, minute=0, second=0)

        # no calendar: try to use the default_interval, then return directly
        if not self:
            working_interval = []
            if default_interval:
                working_interval = (
                    start_dt.replace(
                        hour=default_interval[0], minute=0, second=0),
                    start_dt.replace(
                        hour=default_interval[1], minute=0, second=0))
            intervals = self.interval_remove_leaves(
                working_interval,
                work_limits
            )
            return intervals

        # find leave intervals
        work_intervals = self._get_intervals(start_dt, work_dt, work_limits)

        if leaves is None and compute_leaves:
            leaves = self.get_leave_intervals(resource_id=resource_id)

        # filter according to leaves
        for interval in work_intervals:
            work_intervals = self.interval_remove_leaves(interval, leaves)
            intervals += work_intervals

        return intervals
