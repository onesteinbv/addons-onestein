# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ONESTEiN BV (<http://www.onestein.nl>).
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
    'name': "Task Alert Planner",
    'summary': """Plan task alerts for any date field.""",
    'description': """
    Plan when a task should be created based on a nearing deadline. Any date field can be used. How much time in
    advance the task should be created can be specified.
    """,
    'author': "ONESTEiN BV",
    'website': "http://www.onestein.eu",
    'images': ['static/description/main_screenshot.png'],
    'category': 'Custom',
    'version': '1.0',
    'depends': [
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'task_alert_view.xml',
        'task_alert_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
