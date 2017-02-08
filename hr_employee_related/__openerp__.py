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
    'name': "Employee Relatives",
    'images': ['static/description/main_screenshot.png'],
    'summary': """Store employee relatives for communication.""",
    'description': """
Store employee relatives
========================

This module creates a table for storing eployee relatives for communication
in case of need.

    """,
    'author': "Onestein",
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'hr_employee_related_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
