# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ONESTEiN BV (<http://www.onestein.eu>).
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
    'name': "BI View Editor",
    'summary': """Graphical BI views builder for Odoo 8""",
    'images': ['static/description/main_screenshot.png'],
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'category': 'Reporting',
    'version': '0.1',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'views/bve_view.xml',
        'security/ir.model.access.csv',
        'security/rules.xml'
    ],
    'qweb': [
        'templates.xml'
     ],
    'js': [
        'static/src/js/bve.js'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
