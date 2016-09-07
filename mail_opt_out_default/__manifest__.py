# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Restrict automatic emails to partner',
    'images': [],
    'summary': 'Configure the default value of Opt-Out for new partners',
    'license': 'AGPL-3',
    'author': 'ONESTEiN BV',
    'website': 'http://www.onestein.eu',
    'category': 'Marketing',
    'version': '10.0.1.1.0',
    'depends': [
        'base_setup',
        'mail',
    ],
    'data': [
        'views/res_config_views.xml',
    ]
}
