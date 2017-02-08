# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Address Consolidation",
    'currency': 'EUR',
    'license': 'AGPL-3',
    'images': ['static/description/main_screenshot.png'],
    'summary': """Keep the original partner addresses.""",
    'description': """
Address Consolidation
=====================
Saves the originally used address information for Sale, Stock and Invoicing, and
displays these on the related reports.
    """,
    'author': "Onestein",
    'website': "http://www.onestein.eu",
    'category': 'Sales',
    'version': '1.1.1',
    'depends': [
        'sale_stock',
        'stock',
        'account',
        'sale',
    ],
    'data': [
        'views/account_invoice_view.xml',
        'views/sale_view.xml',
        'views/stock_view.xml',
        'views/report_invoice.xml',
        'views/report_saleorder.xml',
        'views/report_stockpicking.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
