# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerInterest(models.Model):
    _name = "res.partner.interest"

    name = fields.Char(required=True, translate=True)
    partner_ids = fields.Many2many(
        'res.partner',
        'res_partner_interest_rel',
        'interest_id',
        'partner_id',
        'Partners')
    color = fields.Integer('Color Index')
