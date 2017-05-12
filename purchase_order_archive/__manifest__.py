# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Order Archive',
    'summary': 'Archive Purchase Orders',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Purchases',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'views/purchase_order.xml',
    ],
    'installable': True,
}
