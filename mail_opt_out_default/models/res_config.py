# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    default_opt_out = fields.Boolean(
        default=lambda self: self.env.user.company_id.default_opt_out,
        string='Default Opt-out for partners *',
        store=True,
        help='''
        Set the Opt-out value to True by default
        for newly created Partners
        ''',
    )
