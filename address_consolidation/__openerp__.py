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
    'name': "Address Consolidation",
    'summary': """Keep the original partner addresses.
    """,
    'description': """
Address Consolidation
=====================
Saves the originally used address information for Sale, Stock and Invoicing, and
displays these on the respective reports.
    """,
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'category': 'Custom',
    'version': '1.0',
    'depends': [
        'stock',
        'account',
        'sale',
    ],
    'data': [
        'account_invoice_view.xml',
        'sale_view.xml',
        'stock_view.xml',
        'views/report_invoice.xml',
        'views/report_saleorder.xml',
        'views/report_stockpicking.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
