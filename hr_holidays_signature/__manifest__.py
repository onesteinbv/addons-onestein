# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Leave Signature',
    'version': '10.0.1.0.0',
    'sequence': 150,
    'category': 'Human Resources',
    'summary': '',
    'website': '',
    'depends': ['hr_holidays', 'web_draw'],
    'data': [
        'views/hr_holidays_signature.xml'
    ],
    'qweb': [
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
