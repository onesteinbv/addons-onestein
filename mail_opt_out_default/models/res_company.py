# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


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
