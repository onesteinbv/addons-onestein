# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Project Issue Stage',
    'summary': 'Project Issue Stage',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Project Management',
    'version': '8.0.1.0.0',
    'depends': [
        'project',
        'project_issue',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/project_issue_data.xml',
        'views/project_project.xml',
        'views/project_issue.xml',
        'views/project_issue_stage.xml',
        'menu_items.xml',
    ],
}
