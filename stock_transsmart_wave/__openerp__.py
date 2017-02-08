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
    'name': "Transsmart Wave",
    'summary': """Picking Wave support for Transsmart integration""",
    'description': """
Transsmart Wave
===============

This module allows the user to send delivvery orders to transsmart from using the Picking waves

    """,
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Warehouse',
    'version': '1.0',
    'images': ['static/description/main_screenshot.png'],
    'depends': [
        'stock_transsmart',
        'stock_picking_wave'
    ],
    'data': [
        'stock_transsmart_wave_views.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
