# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class account_asset(models.Model):
    _inherit = "account.asset.asset"

    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment")

    @api.model
    def create(self, values):
        context = self.env.context.copy()
        if context.get('default_type', False) == 'in_invoice':
            context.pop('default_type')
        res = super(account_asset, self.with_context(context)).create(values)
        if not self._context.get('internal_call', False) and res.equipment_id:
            ctx = dict(context, internal_call=True)
            res.equipment_id.with_context(ctx).write({'asset_id': res.id})
        return res

    @api.multi
    def write(self, values):
        for asset in self:
            ctx = dict(self.env.context, internal_call=True)
            if not self._context.get('internal_call', False) and \
                    asset.equipment_id:
                asset.equipment_id.with_context(ctx).write({'asset_id': None})
            super(account_asset, asset).write(values)
            if not self._context.get('internal_call', False) and \
                    asset.equipment_id:
                asset.equipment_id.with_context(ctx).write(
                    {'asset_id': asset.id})
        return True
