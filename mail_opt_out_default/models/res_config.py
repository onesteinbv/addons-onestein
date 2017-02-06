# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    default_opt_out = fields.Boolean(
        default=lambda self: self.env.user.company_id.default_opt_out,
        string='Default Opt-out for partners *',
        store=True,
        groups='base.group_system',
        help='''
        Set the Opt-out value to True by default
        for newly created Partners
        ''',
    )

    @api.model
    def create(self, vals):
        res = super(BaseConfigSettings, self).create(vals)
        if 'default_opt_out' in vals:
            new_opt_out = vals.get('default_opt_out')
            existing_opt_out = self.env.user.company_id.default_opt_out
            if new_opt_out != existing_opt_out:
                self.env.user.company_id.default_opt_out = new_opt_out
        return res

    @api.multi
    def write(self, vals):
        res = super(BaseConfigSettings, self).write(vals)
        if 'default_opt_out' in vals:
            new_opt_out = vals.get('default_opt_out')
            existing_opt_out = self.env.user.company_id.default_opt_out
            if new_opt_out != existing_opt_out:
                self.env.user.company_id.default_opt_out = new_opt_out
        return res
