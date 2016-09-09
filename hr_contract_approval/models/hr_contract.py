# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class HRContract(models.Model):
    _inherit = "hr.contract"

    state = fields.Selection(selection_add=[('wait_approval', 'Waiting for Approval')])

    @api.multi
    def write(self, values):
        res = super(HRContract, self).write(values)
        if 'wage' in values:
            for contract in self:
                contract.state = 'draft'
        return res

    @api.multi
    def action_request_approval(self):
        for contract in self:
            contract.state = 'wait_approval'
        return True

    @api.multi
    def action_approve(self):
        for contract in self:
            contract.state = 'open'
        return True

    @api.multi
    def action_disapprove(self):
        for contract in self:
            contract.state = 'close'
        return True

    @api.multi
    def action_reset_to_new(self):
        for contract in self:
            contract.state = 'draft'
        return True

    @api.model
    def check_expiring(self):
        contract_list = self.search([('state','in',['open','pending'])])
        for contract in contract_list:
            # notification
            if contract.date_end and \
                datetime.strptime(contract.date_end[:10],DEFAULT_SERVER_DATE_FORMAT) <= datetime.today() + timedelta(1):
                contract.state = 'close'

    @api.model
    def check_to_renew(self):
        contract_list = self.search([('state', 'in', ['open'])])
        for contract in contract_list:
            # notification
            if contract.date_end and \
                            datetime.strptime(contract.date_end[:10],
                                              DEFAULT_SERVER_DATE_FORMAT) <= datetime.today() + timedelta(7):
                contract.state = 'pending'
