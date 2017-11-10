# -*- coding: utf-8 -*-
# Copyright 2016-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Burgerservicenummer (BSN) for Partners',
    'images': [],
    'version': '11.0.1.0.0',
    'category': 'Localization',
    'author': 'Onestein, Odoo Community Association (OCA)',
    'website': 'http://www.onestein.eu',
    'license': 'AGPL-3',
    'depends': [
        'hr',
    ],
    'data': [
        'views/res_partner.xml',
    ],
    'external_dependencies': {
        'python': ['stdnum'],
    },
}
