# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Cost Spread Auto Post',
    'summary': 'Auto Post spread journal items',
    'version': '11.0.1.1.0',
    'author': 'Onestein',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting',
    'depends': [
        'account_cost_spread',
    ],
    'data': [
        'views/account_invoice_line.xml',
    ],
    'installable': True,
}
