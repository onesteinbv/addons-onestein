# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Project Issue Type',
    'summary': 'Adds field type to project issue',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'version': '10.0.1.0.0',
    'depends': [
        'project',
        'project_issue',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_issue.xml',
        'views/project_issue_type.xml',
        'views/menu.xml',
    ],
}
