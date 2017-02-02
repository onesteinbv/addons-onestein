# -*- coding: utf-8 -*-
# Copyright 2015 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import time
from openerp import models, fields, api, _
from openerp.exceptions import Warning

_logger = logging.getLogger(__name__)


class res_partner_profitseg_segment(models.Model):
    _name = 'res.partner.profitseg.segment'
    _description = 'Customer profit segment'

    name = fields.Char(string="Segment name", size=50, required=True)
    lower_limit = fields.Float(string='Lower limit', required=True)
    upper_limit = fields.Float(string='Upper limit', required=True)
    notes = fields.Text('Additional Information')

    _sql_constraints = [
        ('profit_limit_consistency', 'CHECK(lower_limit < upper_limit)',
            'The lower limit must be lower than the upper one!'),
        ('profit_lower_limit_positive', 'CHECK(lower_limit >= 0)', 'The limit must be positive or zero'),
        ('profit_upper_limit_positive', 'CHECK(upper_limit >= 0)', 'The limit must be positive or zero')
    ]

    def _check_overlap(self, vals, previous_upper=None, previous_lower=None):
        _logger.debug("ONESTEIN res_partner_profitseg_segment _check_overlap")
        if vals.get('lower_limit', False) and vals.get('upper_limit', False):
            if self.search([
                '&', '|', '&', ('upper_limit', '>', vals.get('lower_limit')),
                ('lower_limit', '<=', vals.get('upper_limit')),
                '&', ('lower_limit', '<=', vals.get('upper_limit')),
                ('upper_limit', '>=', vals.get('lower_limit')),
                ('id', '!=', self.id)
            ]):
                raise Warning(_('The segment may not overlap with another.'))
        elif vals.get('lower_limit', False):
            uppers = [segment.upper_limit for segment in self.search([('upper_limit', '<=', previous_lower)])]
            if uppers:
                if vals.get('lower_limit', False) <= max(uppers):
                    raise Warning(_('The segment may not overlap with another.'))
        elif vals.get('upper_limit', False):
            lowers = [segment.lower_limit for segment in self.search([('lower_limit', '>=', previous_upper)])]
            if lowers:
                if vals.get('upper_limit', False) >= min(lowers):
                    raise Warning(_('The segment may not overlap with another.'))
        return True

    @api.multi
    def write(self, vals):
        previous_upper = self.upper_limit
        previous_lower = self.lower_limit
        self._check_overlap(vals, previous_upper=previous_upper, previous_lower=previous_lower)
        return super(res_partner_profitseg_segment, self).write(vals)

    @api.model
    def create(self, vals):
        self._check_overlap(vals)
        return super(res_partner_profitseg_segment, self).create(vals)


class res_partner(models.Model):
    _inherit = 'res.partner'

    profitseg_segment_id = fields.Many2one('res.partner.profitseg.segment',
                                           compute="get_profit_segment", string='Profit segment')

    @api.one
    def get_profit_segment(self):
        _logger.debug("ONESTEiN _get_profit_segment")
        total_turnover = 0.0
        total_cost = 0.0
        for inv_line in self.env['account.invoice.line'].search([
            ('partner_id', '=', self.id),
            ('invoice_id.date_invoice', '>=', time.strftime('%Y-01-01')),
            ('product_id', '!=', False)
        ]):
            total_turnover += inv_line.price_subtotal
            total_cost += inv_line.product_id.standard_price * inv_line.quantity
        profit = total_turnover - total_cost
        # _logger.debug("VALUES {} - {} = {}".format(total_turnover, total_cost, profit))
        segments = self.env['res.partner.profitseg.segment'].search([
            ('lower_limit', '<=', profit),
            ('upper_limit', '>', profit)
        ])
        if segments:
            self.profitseg_segment_id = segments[0].id
        else:
            self.profitseg_segment_id = False
