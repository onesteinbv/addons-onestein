# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Onestein (<http://www.onestein.nl>).
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

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning
import json
import logging

_logger = logging.getLogger(__name__)

def price_from_transsmart_price(price_str):
    """convert transsmart price string to odoo float field."""
    if price_str.startswith('EUR '):
        return float(price_str[4:].replace(',','.'))
    raise Warning(_("Couldn't convert transsmart price %s to float") % (price_str,))

class stock_picking(models.Model):
    _inherit = 'stock.picking'

    delivery_service_level_time_id = fields.Many2one('delivery.service.level.time', string='Delivery Service Level')
    cost_center_id = fields.Many2one('transsmart.cost.center', string='Delivery Cost Center')
    
    delivery_cost = fields.Float('Delivery Cost', digits_compute=dp.get_precision('Product Price'), readonly=True)
    transsmart_id = fields.Integer("Transsmart ID", readonly=True)
    transsmart_confirmed = fields.Boolean("Transsmart Confirmed", compute="_compute_transsmart_confirmed", readonly=True, store=True)

    @api.depends('transsmart_id')
    def _compute_transsmart_confirmed(self):
        for rec in self:
            rec.transsmart_confirmed = bool(rec.transsmart_id)
    
    @api.multi
    def transsmart_carrier_id(self):
        if self.carrier_id and self.carrier_id.partner_id and self.carrier_id.partner_id.transsmart_id: 
            return self.carrier_id.partner_id.transsmart_id
        else:
            return self.env['stock.transsmart.config.settings'].transsmart_default_carrier_id()

    @api.multi
    def transsmart_service_level_time_id(self):
        if self.carrier_id and self.carrier_id.product_id and self.carrier_id.product_id.service_level_time_id:
            return self.carrier_id.product_id.service_level_time_id.transsmart_id
        elif self.delivery_service_level_time_id and self.delivery_service_level_time_id.transsmart_id:
            return self.delivery_service_level_time_id.transsmart_id
        else:
            return self.env['stock.transsmart.config.settings'].transsmart_default_service_level_time_id()

    @api.multi
    def transsmart_cost_center_id(self):
        if self.cost_center_id and self.cost_center_id.transsmart_id:
            return self.cost_center_id.transsmart_id
        else:
            return None


    def _transsmart_document_from_stock_picking(self):
        document = {
            "Reference": filter(unicode.isalnum, self.name),

            # take into account warehouse address, not just company address

            "AddressNamePickup": self.company_id.name or '',
            "AddressStreetPickup": self.company_id.street or '',
            #"AddressStreetNoPickup": "StreetNo",
            "AddressZipcodePickup": self.company_id.zip or '',
            "AddressCityPickup": self.company_id.city or '',
            "AddressCountryPickup": self.company_id.country_id.code or '',


            "AddressName": self.partner_id.name or '',
            "AddressStreet": self.partner_id.street or '',
            #"AddressStreetNo": "StreetNo",
            "AddressZipcode": self.partner_id.zip or '',
            "AddressCity": self.partner_id.city or '',
            "AddressCountry": self.partner_id.country_id.code or '',
            "ColliInformation": [
                {
                    "PackagingType": "BOX",
                    "Description": "Description",
                    "Quantity": 1,
                    "Length": 30,
                    "Width": 30,
                    "Height": 30,
                    "Weight": self.weight or 1
                }
            ],

            "CarrierId": self.transsmart_carrier_id(),
            "ServiceLevelTimeId": self.transsmart_service_level_time_id(),
        }
        if self.transsmart_cost_center_id():
            document.update({
                "CostCenterId": self.transsmart_cost_center_id()
            })

        if self.group_id:
            related_sale = self.env['sale.order'].search([('procurement_group_id','=',self.group_id.id)])

            if related_sale:
                document.update({
                    "AddressNameInvoice": related_sale.partner_invoice_id.name,
                    "AddressStreetInvoice": related_sale.partner_invoice_id.street,
                    #"AddressStreetNoInvoice": "StreetNo",
                    "AddressZipcodeInvoice": related_sale.partner_invoice_id.zip,
                    "AddressCityInvoice": related_sale.partner_invoice_id.city,
                    "AddressCountryInvoice": related_sale.partner_invoice_id.country_id.code,
                })

        return document

    @api.one
    def action_get_transsmart_rate(self):
        if not self.company_id.transsmart_enabled or self.picking_type_id.code != 'outgoing':
            return

        document = self._transsmart_document_from_stock_picking()
        _logger.info("ONESTEiN transsmart.getrates with document: %s" % (json.dumps(document),))
        r = self.env['stock.transsmart.config.settings'].get_transsmart_service().send('/Rates', params={'prebook': 0, 'getrates': 1}, payload=document)[0]
        _logger.info("ONESTEiN transsmart.getrates returned: %s" % (json.dumps(r),))

        carrier = self.env['stock.transsmart.config.settings'].lookup_transsmart_delivery_carrier(r)
        self.write({
            'carrier_id': carrier.id, 
            'delivery_cost': price_from_transsmart_price(r['Price'])
        })

    @api.one
    def action_create_transsmart_document(self):
        if not self.company_id.transsmart_enabled or self.picking_type_id.code != 'outgoing':
            return

        if self.transsmart_id:
            raise Warning(_("This picking is already exported to Transsmart! : ") + self.name)

        document = self._transsmart_document_from_stock_picking()

        _logger.info("ONESTEiN transsmart.document with document: %s" % (json.dumps(document),))
        r = self.env['stock.transsmart.config.settings'].get_transsmart_service().send('/Document', params={'autobook': 1}, payload=document)
        _logger.info("ONESTEiN transsmart.document returned: %s" % (json.dumps(r),))

        carrier = self.env['stock.transsmart.config.settings'].lookup_transsmart_delivery_carrier(r)
        self.write({
            'transsmart_id': r['Id'], 
            'carrier_id': carrier.id, 
            'delivery_cost': r['ShipmentTariff']
        })

    @api.multi
    def action_confirm(self):
        self.action_get_transsmart_rate()
        return super(stock_picking, self).action_confirm()

    @api.model
    def create(self, vals):        
        if 'action_ship_create' in self.env.context:
            vals.update({
                'cost_center_id': self.env.context['action_ship_create'].cost_center_id.id,
                'delivery_service_level_time_id': self.env.context['action_ship_create'].delivery_service_level_time_id.id
            })
        r = super(stock_picking, self).create(vals)
        return r


    def copy(self, cr, uid, ids, defaults=None, context=None):
        if not defaults:
            defaults = {}
        defaults.update({
            'transsmart_confirmed': False,
            'transsmart_id': 0,
            'delivery_cost': 0
        })
        return super(stock_picking, self).copy(cr, uid, ids, defaults, context)
