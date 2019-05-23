# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Disable automatic emails to partner',
    'summary': 'Sets and hides field Opt-Out for all the partners',
    'license': 'AGPL-3',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Marketing',
    'version': '11.0.1.0.0',
    'conflicts': ['mail_opt_out_default'],
    'depends': [
        'mail',
    ],
    'data': [
        'views/res_partner.xml',
    ],
}
