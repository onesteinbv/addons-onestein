# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'HR Holidays leave repeated',
    'summary': 'Adds a flag for defining periodical leaves',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
        'hr_contract',
    ],
    'data': [
        'views/hr_holidays_status.xml',
        'views/hr_holidays_view.xml',
    ],
    'installable': True,
}
