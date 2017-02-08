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


class delivery_service_level(models.Model):
    _name = 'delivery.service.level'

    name = fields.Char(size=128, string="Name")
    code = fields.Char(size=128, string="Code", help="This code should match the code in the Transsmart configuration.")
    transsmart_id = fields.Integer("Transsmart ID")
    description = fields.Char(size=256, string="Description")


class delivery_service_level_time(models.Model):
    _name = 'delivery.service.level.time'

    name = fields.Char(size=128, string="Name")
    transsmart_id = fields.Integer("Transsmart ID")
    code = fields.Char(size=128, string="Code", help="This code should match the code in the Transsmart configuration.")
    description = fields.Char(size=256, string="Description")


class transsmart_cost_center(models.Model):
    _name = 'transsmart.cost.center'

    name = fields.Char(size=128, string="Name")
    transsmart_id = fields.Integer("Transsmart ID")
    code = fields.Char(size=128, string="Code", help="This code should match the code in the Transsmart configuration.")
    description = fields.Char(size=256, string="Description")


class product_product(models.Model):
    _inherit = 'product.product'

    service_level_id = fields.Many2one('delivery.service.level', string='Service Level')
    service_level_time_id = fields.Many2one('delivery.service.level.time', string='Service Level Time')


class res_partner(models.Model):
    _inherit = 'res.partner'

    transsmart_code = fields.Char(size=128, string="Transsmart Code")
    transsmart_id = fields.Integer("Transsmart ID")


class sale_order(models.Model):
    _inherit = 'sale.order'

    delivery_service_level_time_id = fields.Many2one('delivery.service.level.time', string='Delivery Service Level Time')
    cost_center_id = fields.Many2one('transsmart.cost.center', string='Delivery Cost Center')


    def action_ship_create(self, cr, uid, ids, context=None):
        context = context.copy() or {}
        sales = self.browse(cr, uid, ids, context=context)
        context['action_ship_create'] = sales
        r = super(sale_order, self).action_ship_create(cr, uid, ids, context=context)
        for sale in sales:
            sale.picking_ids.action_get_transsmart_rate()
        return r


class res_company(models.Model):
    _inherit = 'res.company'

    transsmart_enabled = fields.Boolean('Use Transsmart', default=True)
