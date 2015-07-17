# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 ONESTEiN BV (<http://www.onestein.nl>).
#              (C) 2014 ICTSTUDIO (<http://www.ictstudio.eu>).
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

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class product_product(osv.osv):
    _inherit = "product.product"
    
    def _check_code(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        else:
            context = context.copy()
        context.update({'active_test': False})
        for product in self.browse(cr, uid, ids, context=context):
            if product.default_code:
                list_product_ids = self.search(cr,uid,[('default_code','=',product.default_code)])
                if self.search(cr,uid,[('default_code','=',product.default_code)]):
                    if len(list_product_ids)==1 and product.id == list_product_ids[0]:
                        return True
                    return False
        return True

    
    def create(self, cr, uid, vals, context=None):

        if context is None:
            context = {}
        else:
            context = context.copy()

        context.update({'active_test': False})

        # Check if sequence exists and assign new number to product
        if vals.get('default_code', '[Auto]') == '[Auto]':
            while True:
                vals['default_code'] = self.pool.get('ir.sequence').next_by_code(cr,
                                                                                 uid,
                                                                                 'product.product',
                                                                                 context=context)
                if self.search(cr,uid,[('default_code','=',vals['default_code'])],context=context):
                    _logger.debug("product get next by code product.product code already exists in database")
                else:
                    break

                ## If no sequence was found

        if vals.get('default_code', '[Auto]') == '[Auto]':
             raise osv.except_osv(
                 _('Error !'),
                 _('No product sequence is defined'))

        return super(product_product, self).create(cr, uid, vals, context)
    
    _columns = {
        'default_code' : fields.char('Internal Reference', select=True),
        }

    _defaults = {
        'default_code': '[Auto]',
        }

    _constraints = [
        (_check_code, 'A product number can only be used once', ['default_code'])
        ]
    
