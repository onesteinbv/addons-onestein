# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Onestein (<http://www.onestein.nl>).
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
    'name': 'Calendar Block',
    'category': 'Website',
    'summary': 'Calendar (based on Messaging -> Calendar) on website.',
    'version': '1.0',
    'description': """
Calendar Block
===============================================
This block is based on Messaging -> Calendar. Use field 'Privacy' to determine publicity.
Since it's a block it can be placed anywhere on your website.
""",
    'author': "Onestein",
    'website': "http://www.onestein.eu",
    'depends': ['website', 'calendar', 'web'],
    'data': [
        'views/website_calendar_block.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}