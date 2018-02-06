# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Holidays expiration',
    'summary': 'Automatic management of holidays expiration. Leave days can have a expiary date per leave type. E-mail warnings can be set.',
    'images': ['static/description/banner.png'],
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Human Resources',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
        'mail',
    ],
    'data': [
        'data/hr_holidays_data.xml',
        'views/hr_holidays.xml',
        'views/res_company.xml',
        'data/hr_holidays_cron.xml',
    ],
}
