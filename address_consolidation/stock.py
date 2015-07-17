# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ONESTEiN BV (<http://www.onestein.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from openerp import models, fields, api
import re

_logger = logging.getLogger(__name__)


class stock_picking(models.Model):
    _inherit = "stock.picking"

    shipping_partner_street = fields.Char('Street')
    shipping_partner_street2 = fields.Char('Street2')
    shipping_partner_zip = fields.Char('Zip', size=24)
    shipping_partner_city = fields.Char('City')
    shipping_partner_state_id = fields.Many2one('res.country.state', string='State')
    shipping_partner_country_id = fields.Many2one('res.country', string='Country')

    @api.multi
    def onchange_partner_id(self, partner_id):
        _logger.debug('ONESTEiN onchange_partner_id')
        res = {'value': {}}

        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            res['value'].update({
                'shipping_partner_street': partner.street,
                'shipping_partner_street2': partner.street2,
                'shipping_partner_zip': partner.zip,
                'shipping_partner_city': partner.city,
                'shipping_partner_state_id': partner.state_id.id,
                'shipping_partner_country_id': partner.country_id.id,
            })
        return res

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, origin, picking=None, context=None):
        """Override method to pass historical address data to invoice.
        Called by stock_picking._invoice_create_line()
        No correct way to get the picking record, so override _invoice_create_line() below.
        """
        _logger.debug("ONESTEiN stock_picking _get_invoice_vals")
        res = super(stock_picking, self)._get_invoice_vals(key, inv_type, journal_id, origin)
        res.update({
            'invoice_partner_street': picking.shipping_partner_street,
            'invoice_partner_street2': picking.shipping_partner_street2,
            'invoice_partner_zip': picking.shipping_partner_zip,
            'invoice_partner_city': picking.shipping_partner_city,
            'invoice_partner_state_id': picking.shipping_partner_state_id.id,
            'invoice_partner_country_id': picking.shipping_partner_country_id.id,
        })
        return res

    @api.model
    def _invoice_create_line(self, moves, journal_id, inv_type='out_invoice', context=None):
        _logger.debug("ONESTEiN stock_picking _invoice_create_line")
        invoice_obj = self.env['account.invoice']
        move_obj = self.env['stock.move']
        invoices = {}
        for move in moves:
            company = move.company_id
            origin = move.picking_id.name
            partner, user_id, currency_id = move_obj._get_master_data(move=move, company=company)

            key = (partner, currency_id, company.id, user_id)

            if key not in invoices:
                # Get account and payment terms
                invoice_vals = self._get_invoice_vals(key, inv_type, journal_id, origin, picking=move.picking_id,
                                                      context=context)
                invoice_id = self._create_invoice_from_picking(move.picking_id, invoice_vals, context=context)
                invoices[key] = invoice_id

            invoice_line_vals = move_obj._get_invoice_line_vals(move, partner, inv_type, context=context)
            invoice_line_vals['invoice_id'] = invoices[key]
            invoice_line_vals['origin'] = origin

            move_obj._create_invoice_line_from_vals(move, invoice_line_vals, context=context)
            move.write({'invoice_state': 'invoiced'})

        invoice_recs = invoice_obj.browse(invoices.values())
        invoice_recs.button_compute(set_total=(inv_type in ('in_invoice', 'in_refund')))
        return invoices.values()

    @api.multi
    def _display_picking_partner_address(self, picking, without_company=False, context=None):
        address_format = picking.partner_id.country_id.address_format or \
            "%(street)s\n%(street2)s\n%(city)s %(state_code)s %(zip)s\n%(country_name)s"

        args = {
            'street': picking.shipping_partner_street or '',
            'street2': picking.shipping_partner_street2 or '',
            'zip': picking.shipping_partner_zip or '',
            'city': picking.shipping_partner_city or '',
            'company_name': picking.partner_id.name or '',
            'state_code': picking.shipping_partner_state_id.code or '',
            'state_name': picking.shipping_partner_state_id.name or '',
            'country_code': picking.shipping_partner_country_id.code or '',
            'country_name': picking.shipping_partner_country_id.name or '',
        }

        if without_company:
            args['company_name'] = ''
        elif picking.partner_id.parent_id:
            address_format = '%(company_name)s\n' + address_format

        res = address_format % args
        res = re.sub("\n\n|\n", "<br/>", res)
        return res


class stock_move(models.Model):
    _inherit = "stock.move"

    @api.model
    def _picking_assign(self, move_ids, procurement_group, location_from, location_to, sale_ids=None, context=None):
        """Assign a picking on the given move_ids, which is a list of move supposed to share the same procurement_group,
        location_from and location_to
        (and company). Those attributes are also given as parameters.
        """
        _logger.debug('ONESTEiN stock_move _picking_assign')
        pick_obj = self.env['stock.picking']
        order_obj = self.env['sale.order']
        picks = pick_obj.search([
            ('group_id', '=', procurement_group),
            ('location_id', '=', location_from),
            ('location_dest_id', '=', location_to),
            ('state', 'in', ['draft', 'confirmed', 'waiting'])])
        if picks:
            pick = picks[0]
        else:
            move = self.browse(move_ids)[0]

            values = {
                'origin': move.origin,
                'company_id': move.company_id and move.company_id.id or False,
                'move_type': move.group_id and move.group_id.move_type or 'direct',
                'partner_id': move.partner_id.id or False,
                'picking_type_id': move.picking_type_id and move.picking_type_id.id or False,
            }

            if sale_ids:
                order = order_obj.browse(sale_ids)

                if order.partner_shipping_id:
                    values.update({
                        'shipping_partner_street': order.shipping_partner_street,
                        'shipping_partner_street2': order.shipping_partner_street2,
                        'shipping_partner_zip': order.shipping_partner_zip,
                        'shipping_partner_city': order.shipping_partner_city,
                        'shipping_partner_state_id': order.shipping_partner_state_id.id,
                        'shipping_partner_country_id': order.shipping_partner_country_id.id,
                    })

            pick = pick_obj.create(values)
        move_rec = self.browse(move_ids)
        return move_rec.write({'picking_id': pick.id})

    def action_confirm(self, cr, uid, ids, sale_ids=None, context=None):
        """Override method to pass sale_id to stock._picking_assign() in order to pass historical
        values when creating picking. Starts with sale_order.action_ship_create().
        Confirms stock move or put it in waiting if it's linked to another move.
        @return: List of ids.
        """
        _logger.debug("ONESTEiN stock_move action_confirm")

        if isinstance(ids, (int, long)):
            ids = [ids]
        states = {
            'confirmed': [],
            'waiting': []
        }
        to_assign = {}
        for move in self.browse(cr, uid, ids, context=context):
            self.attribute_price(cr, uid, move, context=context)
            state = 'confirmed'
            # if the move is preceeded, then it's waiting (if preceeding move is done, then action_assign has been
            # called already and its state is already available)
            if move.move_orig_ids:
                state = 'waiting'
            # if the move is split and some of the ancestor was preceeded, then it's waiting as well
            elif move.split_from:
                move2 = move.split_from
                while move2 and state != 'waiting':
                    if move2.move_orig_ids:
                        state = 'waiting'
                    move2 = move2.split_from
            states[state].append(move.id)

            if not move.picking_id and move.picking_type_id:
                key = (move.group_id.id, move.location_id.id, move.location_dest_id.id)
                if key not in to_assign:
                    to_assign[key] = []
                to_assign[key].append(move.id)

        for move in self.browse(cr, uid, states['confirmed'], context=context):
            if move.procure_method == 'make_to_order':
                self._create_procurement(cr, uid, move, context=context)
                states['waiting'].append(move.id)
                states['confirmed'].remove(move.id)

        for state, write_ids in states.items():
            if len(write_ids):
                self.write(cr, uid, write_ids, {'state': state})
        # assign picking in batch for all confirmed move that share the same details
        for key, move_ids in to_assign.items():
            procurement_group, location_from, location_to = key
            self._picking_assign(cr, uid, move_ids, procurement_group, location_from, location_to, sale_ids=sale_ids,
                                 context=context)
        moves = self.browse(cr, uid, ids, context=context)
        self._push_apply(cr, uid, moves, context=context)
        return ids
