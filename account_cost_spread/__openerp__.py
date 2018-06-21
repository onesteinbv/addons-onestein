# -*- coding: utf-8 -*-
# Copyright 2014 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Cost / Income Spread',
    'summary': 'Cost and Income spreading',
    'version': '8.0.1.0.5',
    'author': 'Onestein',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'images': ['static/description/main_screenshot.png'],
    'category': 'Accounting',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_invoice_line.xml',
        'views/account_invoice.xml',
        'views/account_config_settings.xml',
        'data/spread_cron.xml',
    ],
    'installable': True,
}
