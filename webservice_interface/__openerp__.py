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
    'name': "Web-Services Interface",
    'images': ['static/description/main_screenshot.png'],
    'summary': """Web-Services Interface""",
    'description': """
    Provide to the user methods and structure to easy integrate odoo with several type of web-services
    """,
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Custom',
    'version': '1.0',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'webservice_interface_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
