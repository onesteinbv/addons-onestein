# Copyright 2016-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HRHolidays(models.Model):
    _inherit = "hr.holidays"

    approval_date = fields.Date(string="Date Approved")

    @api.multi
    def action_approve(self):
        res = super(HRHolidays, self).action_approve()
        self.write({'approval_date': fields.Datetime.now()})
        return res

    @api.multi
    def action_draft(self):
        res = super(HRHolidays, self).action_draft()
        self.write({'approval_date': None})
        return res
