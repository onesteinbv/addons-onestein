# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    @api.multi
    def compute_interval(self):
        res = super(HrHolidays, self).compute_interval()
        self.onchange_date()
        return res
