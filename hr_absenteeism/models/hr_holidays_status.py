# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class HrHolidaysStatus(models.Model):
    _inherit = "hr.holidays.status"

    absenteeism_control = fields.Boolean(string="Absence Control")
    notification_ids = fields.One2many(
        "hr.absenteeism.notifications", "leave_type_id", "Notifications")
