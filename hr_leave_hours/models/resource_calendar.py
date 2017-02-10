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

        def set_work_limits_start(end_dt, start_dt):
            work_limits = []
            if start_dt is None and end_dt is not None:
                start_dt = end_dt.replace(
                    hour=0, minute=0, second=0, microsecond=0)
            elif start_dt is None:
                start_dt = datetime.datetime.now().replace(
                    hour=0, minute=0, second=0, microsecond=0)
            else:
                work_limits.append((start_dt.replace(
                    hour=0, minute=0, second=0, microsecond=0), start_dt))
            return start_dt, work_limits

        def set_work_limits_end(end_dt, start_dt, work_limits):
            if end_dt is None:
                end_dt = start_dt.replace(
                    hour=23, minute=59, second=59, microsecond=999999)
            else:
                work_limits.append((end_dt, end_dt.replace(
                    hour=23, minute=59, second=59, microsecond=999999)))
            return end_dt

        start_dt, work_limits = set_work_limits_start(end_dt, start_dt)
        end_dt = set_work_limits_end(end_dt, start_dt, work_limits)
        assert start_dt.date() == end_dt.date(), \
            'get_working_intervals_of_day is restricted to one day'
        return start_dt, work_limits

    @api.multi
    def _get_intervals(self, start_dt, work_dt, work_limits):

        def get_interval(work_day_hour, work_dt):
            interval = work_dt.replace(
                hour=int(work_day_hour),
                minute=int(
                    (work_day_hour - int(work_day_hour)) * 60
                )
            )
            return interval

        work_intervals = []
        for work_day in self.get_attendances_for_weekday(start_dt):
            interval_start = get_interval(work_day.hour_from, work_dt)
            interval_stop = get_interval(work_day.hour_to, work_dt)

            working_interval = (interval_start, interval_stop)
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

        def working_interval(default_interval, start_dt):
            working_interval = []
            if default_interval:
                working_interval = (
                    start_dt.replace(
                        hour=default_interval[0], minute=0, second=0,
                        microsecond=0),
                    start_dt.replace(
                        hour=default_interval[1], minute=0, second=0,
                        microsecond=0))
            return working_interval

        start_dt, work_limits = self._get_work_limits(end_dt, start_dt)

        work_dt = start_dt.replace(hour=0, minute=0, second=0)

        # no calendar: try to use the default_interval, then return directly
        if not self:
            working_interval = working_interval(default_interval, start_dt)
            intervals = self.interval_remove_leaves(
                working_interval,
                work_limits
            )
            return intervals

        # find leave intervals
        work_intervals = self._get_intervals(start_dt, work_dt, work_limits)

        if not leaves and compute_leaves:
            leaves = self.get_leave_intervals(resource_id=resource_id)

        # filter according to leaves
        intervals = []
        for interval in work_intervals:
            work_interval = self.interval_remove_leaves(interval, leaves)
            intervals += work_interval

        return intervals
