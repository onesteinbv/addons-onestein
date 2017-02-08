# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Onestein (<http://www.onestein.nl>).
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
    'name': "Absence Management",
    'summary': """Create time based absence notifications""",
    'description': """
Absense Management
==================
Allows to set up intervals which can be used with the Task Alert module to create a task.
You can set up the intervals in the Human Resources Leave Types Configuration form under the Absence Control header.
To have the tasks created, it is required to set up a Task Alert or a Automated Action on the Absent Notification Date
field.
 """,
    'author': "Onestein",
    'website': "http://www.onestein.eu",
    'images': ['static/description/main_screenshot.png'],
    'category': 'Human Resources',
    'version': '1.0',
    'depends': [
        'hr_holidays',
    ],
    'data': [
        'security/ir.model.access.csv',
        'hr_absenteeism_view.xml',
        'hr_absenteeism_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
