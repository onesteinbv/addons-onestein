# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class HrHolidaysStatus(models.Model):
    _inherit = "hr.holidays.status"

    absenteeism_control = fields.Boolean(string="Absence Control")
    notification_ids = fields.One2many(
        "hr.absenteeism.notifications", "leave_type_id", "Notifications")
