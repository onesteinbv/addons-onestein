# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Christmas Snowflakes',
    'summary': 'Christmas landscape on your Odoo',
    'images': ['static/description/main_screenshot.png'],
    'license': 'AGPL-3',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Web',
    'version': '11.0.1.0.0',
    'depends': [
        'web',
        'web_christmas'
    ],
    'data': [
        'templates/assets.xml',
        'views/res_users_view.xml'
    ],
}
