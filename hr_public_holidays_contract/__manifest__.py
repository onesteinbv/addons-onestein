# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Public Holidays Contract',
    'images': [],
    'summary': '''Public holidays leaves integrated with contracts''',
    'author': 'ONESTEiN BV',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'depends': [
        'hr_public_holidays_leaves',
        'hr_contract',
        'hr_contract_accessibility',  # for access rules on contracts
    ],
    'installable': True,
}
