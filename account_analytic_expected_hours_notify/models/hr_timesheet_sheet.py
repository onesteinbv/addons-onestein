# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api
from openerp.tools.translate import _


class hr_timesheet_sheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    @api.multi
    def button_confirm(self):
        res = super(hr_timesheet_sheet, self).button_confirm()
        accounts_list = []
        for sheet in self:
            for timesheet in sheet.timesheet_ids:
                if timesheet.account_id and timesheet.account_id not in accounts_list:
                    accounts_list += timesheet.account_id
        for account in accounts_list:
            total_hours = 0.0
            for line in account.line_ids:
                total_hours += line.unit_amount
            if (account.limit_hours - total_hours) < 0.0:
                partner_ids = [account.user_id.partner_id.id]
                if account.manager_id and account.manager_id.partner_id.id not in partner_ids:
                    partner_ids.append(account.manager_id.partner_id.id)

                msg = _("Maximum hours for project %s has been reached.") % (account.name)
                self.message_post(body=msg, partner_ids=partner_ids)

        return res
