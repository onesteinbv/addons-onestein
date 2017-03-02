# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    analytic_state = fields.Selection(
        [('draft', 'Draft'),
         ('waiting', 'Waiting for Approval'),
         ('approved', 'Approved'),
         ('expired', 'Expired'),
         ('declined', 'Declined'),
         ('cancel', 'Cancelled')],
        readonly=True,
        default='draft',
        copy=False,
        track_visibility='onchange',
        string="Status")
    date_declined = fields.Date(
        'Date Declined')

    @api.multi
    def action_submit(self):
        for analytic_account in self:
            analytic_account.analytic_state = 'waiting'

    @api.multi
    def action_expire(self):
        for analytic_account in self:
            analytic_account.analytic_state = 'expired'

    @api.multi
    def action_cancel(self):
        for analytic_account in self:
            analytic_account.analytic_state = 'cancel'

    @api.multi
    def action_approve(self):
        for analytic_account in self:
            if analytic_account.analytic_state != 'waiting':
                raise UserError(
                    _('You can only approve Analytic Accounts '
                      'in status Waiting for Approval.'))
            analytic_account.analytic_state = 'approved'

    @api.multi
    def action_decline(self):
        for analytic_account in self:
                analytic_account.analytic_state = 'declined'
                analytic_account.date_declined = fields.Date.today()

    @api.multi
    def action_resubmit(self):
        for analytic_account in self:
            analytic_account.analytic_state = 'waiting'

    @api.multi
    def action_reset_to_draft(self):
        for analytic_account in self:
            analytic_account.analytic_state = 'draft'
