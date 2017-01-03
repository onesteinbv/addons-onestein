# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    """
    This module adds fields to facilitate UI enforcement
    of analytic dimensions.

    Sample code for dimension 'account_analytic_id':

    @api.multi
    def onchange_account_id(self, product_id, partner_id, inv_type,
                            fposition_id, account_id):
        res = super(AccountInvoiceLine, self).onchange_account_id(
            product_id, partner_id, inv_type, fposition_id, account_id)
        account = self.env['account.account'].browse(account_id)
        if account.analytic_dimension_policy == 'never':
            if not res.get('value'):
                res.update({'value': {'account_analytic_id': False}})
            else:
                res['value'].update({'account_analytic_id': False})
        return res

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        account = self.env['account.account'].browse(vals.get('account_id'))
        if account.analytic_dimension_policy == 'never':
            if 'analytic_account_id' in vals:
                del vals['account_analytic_id']
        return super(AccountInvoiceLine, self).create(vals)

    @api.multi
    def write(self, vals):
        for aml in self:
            if 'account_id' in vals:
                account = self.env['account.account'].browse(
                    vals['account_id'])
                if account.analytic_dimension_policy == 'never':
                    vals['account_analytic_id'] = False
        return super(AccountInvoiceLine, self).write(vals)

    """

    costcenter_policy = fields.Selection(
        string='Policy for costcenter dimension',
        related='account_id.costcenter_policy', readonly=True)