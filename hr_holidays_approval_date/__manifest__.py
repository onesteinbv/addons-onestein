# Copyright 2016-2019 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Holidays approval date',
    'summary': 'Add approval date to leaves',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Human Resources',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'hr_holidays',
    ],
    'data': [
        'views/hr_leave.xml',
        'views/hr_leave_allocation.xml',
    ],
}
