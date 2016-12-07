# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class HrAnalyticTimesheet(models.Model):
    _inherit = 'hr.analytic.timesheet'

    @api.multi
    def write(self, values):
        res = super(HrAnalyticTimesheet, self).write(values)
        if 'unit_amount' in values:
            for line in self:
                if line.unit_amount == 0.0:
                    line.unlink()
        return res
