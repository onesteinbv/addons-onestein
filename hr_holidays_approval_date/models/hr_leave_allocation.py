# Copyright 2016-2019 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HRLeaveAllocation(models.Model):
    _inherit = "hr.leave.allocation"

    approval_date = fields.Datetime(string="Date Approved")

    @api.multi
    def action_approve(self):
        res = super().action_approve()
        self.write({'approval_date': fields.Datetime.now()})
        return res

    @api.multi
    def action_draft(self):
        res = super().action_draft()
        self.write({'approval_date': None})
        return res
