# -*- coding: utf-8 -*-
# Copyright 2014-2016 Onestein (<http://www.onestein.eu>)
# Copyright 2014 ICTSTUDIO (<http://www.ictstudio.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner unique reference',
    'currency': 'EUR',
    'license': 'AGPL-3',
    'images': ['static/description/main_screenshot.png'],
    'version': '10.0.1.0.0',
    'summary': '''Generates unique identifiers for partners''',
    'category': 'Extra Tools',
    'author': 'ONESTEiN BV',
    'website': 'http://www.onestein.eu',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/partner_sequence.xml',
        'views/partner_view.xml',
    ],
    'installable': True,
}
