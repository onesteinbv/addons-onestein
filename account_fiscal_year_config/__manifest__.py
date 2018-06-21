# Copyright 2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Fiscal Year Config',
    'summary': 'Fiscal Year configuration views',
    'version': '11.0.1.0.0',
    'author': 'Onestein',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting',
    'depends': [
        'account',
    ],
    'data': [
        'views/res_config_settings.xml',
    ],
    'installable': True,
}
