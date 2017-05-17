# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sales Timesheet Product',
    'summary': 'Invoice timesheets based on employee products',
    'author': 'Onestein',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'images': [],
    'category': 'Sales',
    'version': '10.0.1.0.0',
    'depends': [
        'sale_timesheet',
    ],
    'data': [
        'views/hr_employee.xml',
    ],
    'installable': True,
}
