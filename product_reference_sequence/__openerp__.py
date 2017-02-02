# -*- coding: utf-8 -*-
# Copyright 2014-2017 Onestein (<http://www.onestein.eu>)
# Copyright 2014 ICTSTUDIO (<http://www.ictstudio.eu>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product unique reference',
    'images': ['static/description/main_screenshot.png'],
    'version': '1.1',
    'summary': 'Generates unique identifier for product reference',
    'category': 'Accounting',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'depends': [
        'base',
        'product',
    ],
    'data': [
        'data/product_sequence.xml',
    ],
    'installable': True,
}
