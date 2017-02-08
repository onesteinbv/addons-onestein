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

{
    'name': "Foldable menu",
    'currency': 'EUR',
    'license': 'AGPL-3',
    'images': ['static/description/main_screenshot.png'],
    'summary': """Foldable second level Odoo menu""",
    'description': """
Foldable menu
=============================

This module allows to fold the second level menu items.
    """,
    'author': "Onestein",
    'website': "http://www.onestein.eu",
    'category': "Extra Tools",
    'version': "1.1",
    'depends': ['web'],
    'data': ['views/menu_collapsible.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
