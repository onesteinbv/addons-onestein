# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Costcenter',
    'summary': 'Cost center information for invoice lines',
    'author': 'Onestein',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting',
    'version': '11.0.1.0.0',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/account_cost_center_security.xml',
        'views/account_cost_center.xml',
        'views/account_move.xml',
        'views/account_move_line.xml',
        'views/account_invoice.xml',
        'views/account_invoice_report.xml',
    ],
    'installable': True,
}
