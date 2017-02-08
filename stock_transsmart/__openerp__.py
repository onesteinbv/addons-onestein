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
    'name': "Transsmart Integration",
    'summary': """Transsmart Integration for Odoo8""",
    'description': """
            Transsmart Integration
================================================================

    """,
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Warehouse',
    'version': '1.0.2',
    'images': ['static/description/main_screenshot.png'],
    'depends': [
        'webservice_interface',
        'delivery'
    ],
    'data': [
        "security/ir.model.access.csv",
        "stock_transsmart_views.xml",
        "service_level_views.xml",
        "res_config_views.xml",
        "data/data.xml"
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
