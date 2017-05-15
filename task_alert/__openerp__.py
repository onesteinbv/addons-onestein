# -*- coding: utf-8 -*-
# Copyright 2015 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Task Alert Planner",
    'summary': """Plan task alerts for any date field.""",
    'description': """
    
    This module is obsolete, superseded by module 'project_task_programmed' !

    Plan when a task should be created based on a nearing deadline. Any date field can be used. How much time in
    advance the task should be created can be specified.
    """,
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
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
