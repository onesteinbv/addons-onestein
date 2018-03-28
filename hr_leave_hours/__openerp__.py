# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ONESTEiN BV (<http://www.onestein.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': "Leave Hours",
    'summary': """Leave Request in Hours""",
    'description': """
Leave Hours
===============================================
Request Leaves in Hours and recalculate them to Days. Hide the days in Leave Request.
 """,
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'category': 'Human Resources',
    'version': '0.10',
    'depends': [
        'hr_holidays',
        'hr_contract',
        'hr_holidays_expiration', # for approval_date
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'views/hr_holidays.xml',
        'views/hr_holidays_status.xml',
        'report/hr_holidays_report_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
