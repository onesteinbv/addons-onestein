# -*- coding: utf-8 -*-
# Copyright 2016-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerSequence(models.Model):
    _name = 'res.partner.sequence'

    country_id = fields.Many2one('res.country', 'Country', required=True)
    sequence_id = fields.Many2one('ir.sequence', 'Sequence', required=True)
