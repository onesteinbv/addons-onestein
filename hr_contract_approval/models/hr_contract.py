# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as SDT


class HRContract(models.Model):
    _inherit = "hr.contract"

    state = fields.Selection(
        selection_add=[('wait_approval', 'Waiting for Approval')]
    )

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

    @api.multi
    def action_approve(self):
        for contract in self:
            contract.state = 'open'

    @api.multi
    def action_disapprove(self):
        for contract in self:
            contract.state = 'close'

    @api.multi
    def action_reset_to_new(self):
        for contract in self:
            contract.state = 'draft'

    @api.model
    def _ckeck_date(self, contract, delta):
        if contract.date_end:
            date = datetime.strptime(contract.date_end[:10], SDT)
            return date <= datetime.today() + timedelta(delta)
        return False

    @api.model
    def check_expiring(self):
        contracts = self.search([('state', 'in', ['open', 'pending'])])
        for contract in contracts:
            # notification
            if self._ckeck_date(contract, delta=1):
                contract.state = 'close'

    @api.model
    def check_to_renew(self):
        contracts = self.search([('state', 'in', ['open'])])
        for contract in contracts:
            # notification
            if self._ckeck_date(contract, delta=7):
                contract.state = 'pending'
