# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Holidays expiration",
    'summary': """Automatic management of holidays expiration""",
    'images': [],
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '8.0.1.0.0',
    'depends': [
        'hr_holidays',
        'email_template',
    ],
    'data': [
        'data/hr_holidays_data.xml',
        'views/hr_holidays.xml',
        'views/res_company.xml',
        'data/hr_holidays_cron.xml',
    ],
}
