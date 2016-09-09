# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Human Resource Contract Approval",
    'summary': """Human Resource Contract Approval""",
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'depends': [
        'hr_contract',
    ],
    'data': [
        'data/hr_contract_cron.xml',
        'security/res_groups.xml',
        'views/hr_contract.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
