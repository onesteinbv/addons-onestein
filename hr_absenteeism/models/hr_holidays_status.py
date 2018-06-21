# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrHolidaysStatus(models.Model):
    _inherit = "hr.holidays.status"

    absenteeism_control = fields.Boolean(string="Absence Control")
    notification_ids = fields.One2many(
        "hr.absenteeism.notifications", "leave_type_id", "Notifications")
