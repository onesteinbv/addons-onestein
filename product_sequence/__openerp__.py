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

{
    'name': 'Product sequence',
    'version': '1.0.1',
    'summary': """Generates unique identifiers for products""",
    'category': 'Custom',
    'description': """
Product sequence
===============================================
Adding Product Sequence to the default_code field
""",
    'author': 'ONESTEiN BV',
    'website': 'http://www.onestein.eu',
    'depends': [
        'base',
        'product',
    ],
    'data': [
        'product_sequence.xml',
    ],
    
    'installable': True,
    'application': True,
}
