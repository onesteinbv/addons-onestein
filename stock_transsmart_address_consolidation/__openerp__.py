# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Onestein (<http://www.onestein.nl>).
#              (C) 2015 1200wd.com
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

{
    'name': "Transsmart Address Consolidation",
    'summary': """Address Consolidation support for Transsmart integration""",
    'description': """
    Transsmart Address Consolidation
================================================================

Integrates stock_transsmart with address_consolidation
Uses the denormalized address from address_consolidation in all
stock_transsmart communication instead off the standard res_partner_address.

    """,
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Warehouse',
    'version': '1.0',
    'images': ['static/description/main_screenshot.png'],
    'depends': [
        'stock_transsmart',
        'address_consolidation'
    ],
    'data': [
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
