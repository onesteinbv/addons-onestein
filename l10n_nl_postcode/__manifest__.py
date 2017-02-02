# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Postcode validation for Partners',
    'images': [],
    'version': '10.0.0.1.0',
    'category': 'Localization',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'external_dependencies': {
        'python': ['stdnum'],
    },
    'post_init_hook': 'post_init_hook',
}
