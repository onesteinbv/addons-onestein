# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class account_analytic_account(models.Model):

    _inherit = 'account.analytic.account'

    @api.multi
    def _get_limit_hours(self):
        for account in self:
            account.limit_hours = account.quantity_max

    alert_writing_hours = fields.Selection([
            ('no_block', 'No Block'),
            ('block', 'Block'),
            ('alert', 'Alert'),
        ],
        default='no_block',
        string="Writing hours on reaching expected hours",
        required=True)

    limit_hours = fields.Float(compute='_get_limit_hours', string='Limit Hours')
    limit_percentage = fields.Float(string='Limit Percentage (Block/Alert on expected hours)')

    limit_date_start = fields.Date(string='Date Start')
    limit_date_end = fields.Date(string='Date End')
