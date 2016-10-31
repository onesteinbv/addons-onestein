# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Disable automatic emails to partner',
    'images': [],
    'summary': 'Sets and hides field Opt-Out for all the partners',
    'license': 'AGPL-3',
    'author': 'ONESTEiN BV',
    'website': 'http://www.onestein.eu',
    'category': 'Marketing',
    'version': '10.0.1.0.0',
    'conflicts': ['mail_opt_out_default'],
    'depends': [
        'mail',
    ],
    'data': [
        'views/res_partner.xml',
    ],
}
