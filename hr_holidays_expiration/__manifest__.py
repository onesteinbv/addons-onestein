# Copyright 2016-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Holidays expiration',
    'summary': 'Automatic management of holidays expiration',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Human Resources',
    'version': '11.0.2.0.0',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
        'mail',
    ],
    'data': [
        'data/hr_holidays_data.xml',
        'data/hr_holidays_cron.xml',
        'views/hr_holidays.xml',
        'views/res_config_settings_views.xml',
        'wizards/wizard_hr_holidays_status_archive.xml',
    ],
}
