# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    @api.model
    def create(self, vals):
        if not self._context.get('skip_sequence_creation', False):
            company_id = vals.get('company_id', False)
            if not company_id:
                company_id = self.env.user.company_id.id
            Sequence = self.env['ir.sequence']
            number = Sequence.with_context(
                force_company=company_id
            ).next_by_code('account.analytic.account')
            vals['code'] = number or '/'
        return super(AccountAnalyticAccount, self).create(vals)

    _sql_constraints = [
        ('code',
         'unique (code,company_id)',
         'Reference must be unique per company!')
    ]
