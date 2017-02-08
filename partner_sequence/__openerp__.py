# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Onestein (<http://www.onestein.nl>).
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
    'name': 'Partner unique reference',
    'currency': 'EUR',
    'license': 'AGPL-3',
    'images': ['static/description/main_screenshot.png'],
    'version': '1.1',
    'summary': """Generates unique identifiers for partners""",
    'category': 'Extra Tools',
    'description': """
Partner sequence
===============================================
Use the standard reference field on the partner form as a unique partner number.
Adds extra sequence type: 'Partner' and a sequence with code on res.partner. 
As default this sequence will be used to assign to partners. 
The partner reference will be added to the partner just like the reference for a product in Odoo.
""",
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'partner_view.xml',
        'partner_sequence.xml',
    ],
    'installable': True,
    'application': False,
}
