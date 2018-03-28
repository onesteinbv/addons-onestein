# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from operator import itemgetter

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.float_utils import float_compare
from openerp.tools.translate import _

class resource_calendar(osv.osv):
    _inherit = "resource.calendar"

    def get_working_intervals_of_day(self, cr, uid, id, start_dt=None, end_dt=None,
                                     leaves=None, compute_leaves=False, resource_id=None,
                                     default_interval=None, context=None):
        """ Copied method because of the working intervals not calculating the minutes only the hours"""
        if isinstance(id, (list, tuple)):
            id = id[0]

        # Computes start_dt, end_dt (with default values if not set) + off-interval work limits
        work_limits = []
        if start_dt is None and end_dt is not None:
            start_dt = end_dt.replace(hour=0, minute=0, second=0)
        elif start_dt is None:
            start_dt = datetime.datetime.now().replace(hour=0, minute=0, second=0)
        else:
            work_limits.append((start_dt.replace(hour=0, minute=0, second=0), start_dt))
        if end_dt is None:
            end_dt = start_dt.replace(hour=23, minute=59, second=59)
        else:
            work_limits.append((end_dt, end_dt.replace(hour=23, minute=59, second=59)))
        assert start_dt.date() == end_dt.date(), 'get_working_intervals_of_day is restricted to one day'

        intervals = []
        work_dt = start_dt.replace(hour=0, minute=0, second=0)

        # no calendar: try to use the default_interval, then return directly
        if id is None:
            if default_interval:
                working_interval = (start_dt.replace(hour=default_interval[0], minute=0, second=0), start_dt.replace(hour=default_interval[1], minute=0, second=0))
            intervals = self.interval_remove_leaves(working_interval, work_limits)
            return intervals

        working_intervals = []
        for calendar_working_day in self.get_attendances_for_weekdays(cr, uid, id, [start_dt.weekday()], context):
            working_interval = (
                work_dt.replace(hour=int(calendar_working_day.hour_from), minute=int((calendar_working_day.hour_from-int(calendar_working_day.hour_from))*60)),
                work_dt.replace(hour=int(calendar_working_day.hour_to), minute=int((calendar_working_day.hour_to-int(calendar_working_day.hour_to))*60))
            )
            working_intervals += self.interval_remove_leaves(working_interval, work_limits)

        # find leave intervals
        if leaves is None and compute_leaves:
            leaves = self.get_leave_intervals(cr, uid, id, resource_id=resource_id, context=None)

        # filter according to leaves
        for interval in working_intervals:
            work_intervals = self.interval_remove_leaves(interval, leaves)
            intervals += work_intervals

        return intervals
