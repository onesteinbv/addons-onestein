# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    default_opt_out = fields.Boolean(
        default=True,
        string='Enable Opt-out by default',
        help='''
        Set the Opt-out value to True by default
        for newly created Partners
        ''',
    )
