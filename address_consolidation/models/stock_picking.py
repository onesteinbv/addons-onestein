# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import re


class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipping_partner_street = fields.Char('Street')
    shipping_partner_street2 = fields.Char('Street2')
    shipping_partner_zip = fields.Char('Zip', size=24)
    shipping_partner_city = fields.Char('City')
    shipping_partner_state_id = fields.Many2one('res.country.state', string='State')
    shipping_partner_country_id = fields.Many2one('res.country', string='Country')

    @api.multi
    def onchange_partner_id(self, partner_id):

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
    def _get_invoice_vals(self, key, inv_type, journal_id, move, picking=None):
        """Override method to pass historical address data to invoice.
        Called by stock_picking._invoice_create_line()
        No correct way to get the picking record, so override _invoice_create_line() below.
        """
        res = super(StockPicking, self)._get_invoice_vals(key, inv_type, journal_id, move)
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
        invoice_obj = self.env['account.invoice']
        move_obj = self.env['stock.move']
        invoices = {}
        for move in moves:
            company = move.company_id
            origin = move.picking_id.name
            partner, user_id, currency_id = move_obj._get_master_data(move=move, company=company)

            key = (partner, currency_id, company.id, user_id) # works with standard Odoo
            # key = (partner, currency_id, company.id) # Adaptation for OCB

            if key not in invoices:
                # Get account and payment terms
                invoice_vals = self._get_invoice_vals(key, inv_type, journal_id, move, picking=move.picking_id)
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
