# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

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
            name = record.name
            if not record.limit:
                name = name + (
                    '  (%.1f Left / %.1f Virtually Left' % (
                        record.remaining_hours,
                        record.virtual_remaining_hours
                    )
                )
                if record.expiration_date:
                    try:
                        name = name + (
                            ' - Exp. Date %s)' % (
                                datetime.strptime(
                                    record.expiration_date,
                                    '%Y-%m-%d'
                                ).strftime('%m/%d/%Y')
                            )
                        )
                    except:
                        name = name + (
                            ' - Exp. Date %s)' % (
                                record.expiration_date
                            )
                        )
                else:
                    name = name + ')'
            res.append((record.id, name))
        return res
