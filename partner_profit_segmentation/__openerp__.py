# -*- coding: utf-8 -*-
# Copyright 2015 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Customer profit segmentation',
    'images': ['static/description/main_screenshot.png'],
    'summary': 'Customer segmentation based on profit',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Sales',
    'version': '8.0.1.0.0',
    'depends': ['base', 'account', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'res_partner_profitseg_view.xml',
    ],
    'installable': True,
}
