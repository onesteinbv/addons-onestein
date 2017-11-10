# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'NL Tax Invoice Basis (Factuurstelsel)',
    'summary': 'Enable invoice basis on tax according to the Dutch law',
    'version': '11.0.1.0.0',
    'category': 'Localization',
    'author': 'Onestein, Odoo Community Association (OCA)',
    'website': 'http://www.onestein.eu',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_tax_balance',
    ],
    'data': [
        'views/res_config_settings.xml',
    ],
    'installable': True,
}
