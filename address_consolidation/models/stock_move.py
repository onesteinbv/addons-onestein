# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import re


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _picking_assign(self, move_ids, procurement_group, location_from, location_to, context=None):
        """Assign a picking on the given move_ids, which is a list of move supposed to share the same procurement_group,
        location_from and location_to
        (and company). Those attributes are also given as parameters.
        """
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

            if self._context.get('sale_ids', None):
                order = order_obj.browse(self._context['sale_ids'])

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

    def action_confirm(self, cr, uid, ids, context=None):
        """Override method to pass sale_id to stock._picking_assign() in order to pass historical
        values when creating picking. Starts with sale_order.action_ship_create().
        Confirms stock move or put it in waiting if it's linked to another move.
        @return: List of ids.
        """

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
            self._picking_assign(cr, uid, move_ids, procurement_group, location_from, location_to,
                                 context=context)
        moves = self.browse(cr, uid, ids, context=context)
        self._push_apply(cr, uid, moves, context=context)
        return ids
