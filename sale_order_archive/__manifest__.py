# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Order Archive',
    'summary': 'Archive Sale Orders',
    'author': 'Onestein, Odoo Community Association (OCA)',
    'website': 'http://www.onestein.eu',
    'category': 'Sales',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'views/sale_order.xml',
    ],
    'installable': True,
}
