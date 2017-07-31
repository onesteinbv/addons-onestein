# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _has_user_group_interest(self):
        has_group = self.env['res.users'].has_group(
            'crm_tags_interest.group_res_partner_interest')
        for partner in self:
            partner.has_user_group_interest = has_group

    has_user_group_interest = fields.Boolean(
        compute='_has_user_group_interest')
    interest_ids = fields.Many2many(
        'res.partner.interest',
        'res_partner_interest_rel',
        'partner_id',
        'interest_id',
        'Interests')
    contact_interest_ids = fields.Many2many(
        related='parent_id.interest_ids',
        string='Interests')
