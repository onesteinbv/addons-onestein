# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

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
    date_declined = fields.Date()

    @api.multi
    def action_submit(self):
        self.write({'analytic_state': 'waiting'})

    @api.multi
    def action_expire(self):
        self.write({'analytic_state': 'expired'})

    @api.multi
    def action_cancel(self):
        self.write({'analytic_state': 'cancel'})

    @api.multi
    def action_approve(self):
        for analytic_account in self:
            if analytic_account.analytic_state != 'waiting':
                raise UserError(
                    _('You can only approve Analytic Accounts '
                      'in status Waiting for Approval.'))
        self.write({'analytic_state': 'approved'})

    @api.multi
    def action_decline(self):
        self.write({
            'analytic_state': 'declined',
            'date_declined': fields.Date.today(),
        })

    @api.multi
    def action_resubmit(self):
        self.write({'analytic_state': 'waiting'})

    @api.multi
    def action_reset_to_draft(self):
        self.write({'analytic_state': 'draft'})
