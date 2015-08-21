# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ONESTEiN BV (<http://www.onestein.nl>).
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
    'name': 'Mass mailing unsubscription',
    'images': ['static/desciption/main_screenshot.png'],
    'summary': """Configurable unsubscribe possibility for mass mailing""",
    'description': """
Mass mailing unsubscribe
========================
This module lets you configure whether you want to have the standard unsubscribe link or
add your own link to the mass mailing emails.
""",
    'version': '1.1',
    'author': 'ONESTEiN BV',
    'website': 'http://onestein.eu',
    'category': 'Extra Tools',
    'depends': [
        'mass_mailing'
    ],
    'data': [
        'mail_view.xml'
    ],
    'qweb': [
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
}
