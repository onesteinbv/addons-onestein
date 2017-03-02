# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo import api, fields, models


class HrHolidaysStatus(models.Model):
    _inherit = "hr.holidays.status"
    _order = 'expiration_date asc'

    expiration_date = fields.Date(string="Expiration Date")

    @api.multi
    def name_get(self):
        if not self._context.get('employee_id', False):
            # leave counts is based on employee_id,
            # would be inaccurate if not based on correct employee
            return super(HrHolidaysStatus, self).name_get()

        res = []
        for record in self:
            record._set_name(res)
        return res

    @api.multi
    def _set_name(self, res):
        self.ensure_one()

        name = self.name
        if not self.limit:
            name = name + (
                '  (%.1f Left / %.1f Virtually Left' % (
                    self.remaining_hours,
                    self.virtual_remaining_hours
                )
            )
            if self.expiration_date:
                name = name + (
                    ' - Exp. Date %s)' % (
                        datetime.strptime(
                            self.expiration_date,
                            DF
                        ).strftime(DF)
                    )
                )
            else:
                name = name + ')'
        res.append((self.id, name))
