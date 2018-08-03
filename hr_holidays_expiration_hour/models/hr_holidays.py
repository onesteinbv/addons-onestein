# Copyright 2016-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class HRHolidays(models.Model):
    _inherit = "hr.holidays"

    @api.multi
    def _get_duration(self):
        self.ensure_one()
        return self.number_of_hours_temp

    @api.multi
    def _set_duration(self, duration):
        self.ensure_one()
        self.number_of_hours_temp = duration
