# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 ONESTEiN BV (<http://www.onestein.nl>).
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

from openerp.osv import orm, fields


class Config(orm.TransientModel):
    _inherit = 'account.config.settings'

    _columns = {
        'module_account_cost_spread': fields.boolean(
            'Cost spreading on Invoices',
            help="""This will allow you to spread the cost of an invoice.
                    The module account_cost spread will be installed."""),
    }
