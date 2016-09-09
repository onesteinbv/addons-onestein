# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "HR Contracts Accessibility",
    'summary': """HR Contracts Accessibility""",
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': [
        'hr_contract',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_user_own.xml',
    ],
}
