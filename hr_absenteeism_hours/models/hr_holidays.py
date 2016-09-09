# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    @api.multi
    def compute_interval(self):
        res = super(HrHolidays, self).compute_interval()
        self.onchange_date()
        return res
