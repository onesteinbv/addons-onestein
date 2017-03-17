# -*- coding: utf-8 -*-
# Copyright 2014-2017 Onestein (<http://www.onestein.eu>)
# Copyright 2014 ICTSTUDIO (<http://www.ictstudio.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ref = fields.Char(
        'Reference',
        required=True,
        default='[Auto]',
        index=True
    )

    @api.constrains('ref')
    def _check_ref(self):
        for partner in self:
            if partner.is_company and partner.ref:
                partner._check_ref_raise_error()

    @api.multi
    def _check_ref_raise_error(self):
        self.ensure_one()
        partners = self.with_context(active_test=False).search([
            ('ref', '=', self.ref)
        ])
        if partners and (len(partners) > 1 or self.id != partners.id):
            msg = _('A customer number can only be used once.')
            raise ValidationError(msg)

    @api.model
    def _check_create_seq_country(self, vals):
        if vals.get('ref', '[Auto]') == '[Auto]':
            if 'country_id' in vals:
                PartnerSequence = self.env['res.partner.sequence']
                partner_sequence_id = PartnerSequence.search([
                    ('country_id', '=', vals['country_id'])
                ], limit=1)
                if partner_sequence_id:
                    sequence = partner_sequence_id.sequence_id
                    if sequence:
                        while True:
                            vals['ref'] = sequence.next_by_id()
                            partners = self._get_partners_with_ref(vals['ref'])
                            if not partners:
                                break

    @api.model
    def _check_create_seq_default(self, vals):
        if vals.get('ref', '[Auto]') == '[Auto]':
            while True:
                Sequence = self.env['ir.sequence']
                vals['ref'] = Sequence.next_by_code('res.partner')
                partners = self._get_partners_with_ref(vals['ref'])
                if not partners:
                    break

    @api.model
    def create(self, vals):
        # Check if sequence exists for specific country, and get a new number
        self._check_create_seq_country(vals)

        # If no number was found with the specific country approach
        # the default sequence will be used
        self._check_create_seq_default(vals)

        # If no sequence was found
        if 'ref' not in vals or not vals['ref'] or vals['ref'] == '[Auto]':
            raise UserError(_('No partner sequence is defined'))

        return super(ResPartner, self).create(vals)

    @api.model
    def _get_partners_with_ref(self, ref):
        partners = self.with_context(active_test=False).search([
            ('ref', '=', ref)
        ], limit=1)
        return partners
