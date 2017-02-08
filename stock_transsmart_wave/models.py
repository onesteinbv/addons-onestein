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

class stock_picking_wave(models.Model):
    _inherit = "stock.picking.wave"

    transsmart_confirmed = fields.Boolean("Transsmart Confirmed", 
                     compute="_compute_transsmart_confirmed", readonly=True)

    @api.depends('picking_ids')
    def _compute_transsmart_confirmed(self):
        for rec in self:
            rec.transsmart_confirmed = all([bool(picking.transsmart_id) 
                                           for picking in self.picking_ids]) 


    @api.one
    def action_create_transsmart_document(self):
        for picking in self.picking_ids:
            if not picking.transsmart_confirmed:
                picking.action_create_transsmart_document()


class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    def _transsmart_document_from_stock_picking(self):
        """Add wave reference to transsmart document.
        """
        document = super(stock_picking, 
                         self)._transsmart_document_from_stock_picking()
        document.update({
            "RefOther": self.wave_id and self.wave_id.name or ''
        })
        return document
