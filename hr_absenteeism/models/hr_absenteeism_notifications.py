# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrAbsenteeismNotifications(models.Model):
    _name = "hr.absenteeism.notifications"
    _description = "Absenteeism Notifications"

    name = fields.Char("Notification Name")
    interval = fields.Integer("Interval (days)")
    leave_type_id = fields.Many2one(
        "hr.holidays.status", string="Leave Type", readonly=True)
