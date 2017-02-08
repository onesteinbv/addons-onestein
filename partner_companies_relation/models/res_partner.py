# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_parent_id = fields.Many2one(
        'res.partner',
        'Related Organization',
        select=True,
    )
    company_child_ids = fields.One2many(
        'res.partner',
        'company_parent_id',
        'Related Organizations',
        domain=[('active', '=', True)],
    )
