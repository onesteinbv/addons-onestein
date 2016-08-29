# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class hr_absenteeism_notifications(models.Model):
    _name = "hr.absenteeism.notifications"
    _description = "Absenteeism Notifications"

    name = fields.Char("Notification Name")
    interval = fields.Integer("Interval (days)")
    leave_type_id = fields.Many2one(
        "hr.holidays.status", string="Leave Type", readonly=True)
