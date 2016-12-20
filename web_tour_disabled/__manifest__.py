# -*- coding: utf-8 -*-
# Copyright 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Web Tours Disabled',
    'summary': '''Hide the animations of the Odoo Web Tours''',
    'license': 'AGPL-3',
    'author': 'ONESTEiN BV',
    'website': 'http://www.onestein.eu',
    'category': 'Web',
    'version': '10.0.1.0.0',
    'depends': [
        'web',
        'web_tour',
    ],
    'data': [
        'views/tour_templates.xml',
    ],
}
