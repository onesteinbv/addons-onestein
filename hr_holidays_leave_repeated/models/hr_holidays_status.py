# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class hr_holidays_status(models.Model):
    _inherit = "hr.holidays.status"

    repeat = fields.Boolean(
        'Repeating',
        states={'draft': [('readonly', False)]},
        default=False
    )
