# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Human Resource Contract Approval',
    'summary': 'Human Resource Contract Approval',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'hr_contract',
    ],
    'data': [
        'data/hr_contract_cron.xml',
        'security/res_groups.xml',
        'views/hr_contract.xml',
    ],
    'installable': True,
}
