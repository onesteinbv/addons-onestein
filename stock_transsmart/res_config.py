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
import logging

_logger = logging.getLogger(__name__)

class stock_transsmart_configuration(models.TransientModel):
    _name = 'stock.transsmart.config.settings'
    _inherit = 'res.config.settings'

    service_level_time_id = fields.Many2one('delivery.service.level.time', string='Default Prebooking Service Level Time',                        
                                        help='Default service level time.')
    carrier_id = fields.Many2one('res.partner', string='Default Prebooking Carrier',                        
                                 help='Default carrier.')
    disable = fields.Boolean('Disable')

    @api.multi
    def get_default_transsmart(self):
        return {'carrier_id': self.env['ir.model.data'].xmlid_to_object('stock_transsmart.transsmart_default_carrier').res_id,
                'service_level_time_id': self.env['ir.model.data'].xmlid_to_object('stock_transsmart.transsmart_default_service_level').res_id,
            }
   
    @api.multi
    def transsmart_default_carrier_id(self):
        carrier_id = self.env['ir.model.data'].xmlid_to_object('stock_transsmart.transsmart_default_carrier').res_id
        if not carrier_id:
            return None
        carrier = self.env['res.partner'].browse([carrier_id])[0]
        return carrier.transsmart_id

    @api.multi
    def transsmart_default_service_level_time_id(self):
        service_id = self.env['ir.model.data'].xmlid_to_object('stock_transsmart.transsmart_default_service_level').res_id
        if not service_id:
            return None
        service = self.env['delivery.service.level.time'].browse([service_id])[0]
        return service.transsmart_id

    @api.multi
    def set_transsmart_defaults(self):
        self.env['ir.model.data'].xmlid_to_object('stock_transsmart.transsmart_default_carrier').write({
            'res_id': self.carrier_id and self.carrier_id.id or None
        })
        self.env['ir.model.data'].xmlid_to_object('stock_transsmart.transsmart_default_service_level').write({
            'res_id': self.service_level_time_id and self.service_level_time_id.id or None
        })

    def get_transsmart_service(self):
        return self.env['ir.model.data'].get_object('stock_transsmart', 'web_service_transsmart')

    def get_transsmart_carrier_tag(self):
        return self.env['ir.model.data'].get_object('stock_transsmart', 'res_partner_category_transsmart_carrier')        

    @api.multi
    def sync_transsmart_models(self):
        remote_data = self.get_transsmart_service().receive('/ServiceLevelOther')
        local_data = self.env['delivery.service.level'].search([])
        local_codes = {local.code: local for local in local_data}
        for data in remote_data:
            if not data['Code'] in local_codes:
                self.env['delivery.service.level'].create({
                    'code': data['Code'], 
                    'name': data['Name'], 
                    'transsmart_id': data['Id']})
                _logger.info("ONESTEiN Created transsmart delivery.service.level %s" % (data['Code'],))
            else:
                local_codes[data['Code']].write({
                    'code': data['Code'], 
                    'name': data['Name'], 
                    'transsmart_id': data['Id']})

        remote_data = self.get_transsmart_service().receive('/ServiceLevelTime')
        local_data = self.env['delivery.service.level.time'].search([])
        local_codes = {local.code: local for local in local_data}
        for data in remote_data:
            if not data['Code'] in local_codes:
                self.env['delivery.service.level.time'].create({
                    'code': data['Code'], 
                    'name': data['Name'], 
                    'transsmart_id': data['Id']})
                _logger.info("ONESTEiN Created transsmart delivery.service.level.time %s" % (data['Code'],))
            else:
                local_codes[data['Code']].write({
                    'code': data['Code'], 
                    'name': data['Name'], 
                    'transsmart_id': data['Id']})

        remote_data = self.get_transsmart_service().receive('/Carrier')
        local_data = self.env['res.partner'].search([])
        local_codes = {local.transsmart_code: local for local in local_data}
        for data in remote_data:
            if not data['Code'] in local_codes:
                self.env['res.partner'].create({
                    'transsmart_code': data['Code'], 
                    'name': data['Name'], 
                    'supplier': True, 
                    'customer': False,
                    'is_company': True, 
                    'transsmart_id': data['Id'],
                    'category_id': [(4,self.get_transsmart_carrier_tag().id)]})
                _logger.info("ONESTEiN Created transsmart res.partner %s" % (data['Code'],))
            else:
                local_codes[data['Code']].write({
                    'transsmart_code': data['Code'], 
                    'name': data['Name'], 
                    'supplier': True, 
                    'is_company': True, 
                    'transsmart_id': data['Id'],
                    'category_id': [(4,self.get_transsmart_carrier_tag().id)]})

        remote_data = self.get_transsmart_service().receive('/Costcenter')
        local_data = self.env['transsmart.cost.center'].search([])
        local_codes = {local.code: local for local in local_data}
        for data in remote_data:
            if not data['Code'] in local_codes:
                self.env['transsmart.cost.center'].create({
                    'code': data['Code'], 
                    'name': data['Name'], 
                    'transsmart_id': data['Id']})
                _logger.info("ONESTEiN Created transsmart.cost.center %s" % (data['Code'],))
            else:
                local_codes[data['Code']].write({
                    'code': data['Code'], 
                    'name': data['Name'], 
                    'transsmart_id': data['Id']})


    @api.multi
    def lookup_transsmart_delivery_carrier(self, transsmart_document):
        if 'ServiceLevelOtherId' not in transsmart_document:
            raise Warning(_('No Service Level Other Id found in Transsmart Document'))
        service_level_other = self.env['delivery.service.level'].search([('transsmart_id','=',transsmart_document['ServiceLevelOtherId'])])
        if len(service_level_other) != 1:
            raise Warning(_('No unique Service Level Other found with transsmart Id %s: You have to refresh or review the transsmart data!') % (transsmart_document['ServiceLevelOtherId'],))

        if 'ServiceLevelTimeId' not in transsmart_document:
            raise Warning(_('No Service Level Time Id found in Transsmart Document'))
        service_level_time = self.env['delivery.service.level.time'].search([('transsmart_id','=',transsmart_document['ServiceLevelTimeId'])])
        if len(service_level_time) != 1:
            raise Warning(_('No unique Service Level Time found with transsmart Id %s: You have to refresh or review the transsmart data!') % (transsmart_document['ServiceLevelTimeId'],))

        if 'CarrierId' not in transsmart_document:
            raise Warning(_('No Carrier Id found in Transsmart Document'))
        carrier = self.env['res.partner'].search([('transsmart_id','=',transsmart_document['CarrierId'])])
        if len(carrier) != 1:
            raise Warning(_('No unique Carrier found with transsmart Id %s: You have to refresh or review the transsmart data!') % (transsmart_document['CarrierId'],))

        products = self.env['product.product'].search([
            ('service_level_id', '=', service_level_other[0].id), 
            ('service_level_time_id', '=', service_level_time[0].id)
        ])
        if len(products) < 1:
            # autocreate product
            products = [self.env['product.product'].create({
                'name': transsmart_document['Carrier'],
                'type': 'service',
                'service_level_id': service_level_other[0].id, 
                'service_level_time_id': service_level_time[0].id

            })]

        delivery_carrier = self.env['delivery.carrier'].search([('partner_id','=', carrier[0].id), ('product_id','=',products[0].id)])
        if len(delivery_carrier) < 1:
            # autcreate delivery.carrier
            delivery_carrier = self.env['delivery.carrier'].create({
                'name': transsmart_document['Carrier'],
                'partner_id': carrier[0].id,
                'product_id': products[0].id
            })

        return delivery_carrier[0]
