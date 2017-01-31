# -*- coding: utf-8 -*-
# Copyright 2015 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Project CRM Phone Calls',
    'summary': '''Easily convert a call to an Opportunity or an Issue''',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Project Management',
    'version': '8.0.1.0.0',
    'depends': [
        'crm_project_issue',

        # for filling analytic_account_id in project.issue
        # TODO create a separate autoinstall module to handle this
        'project_issue_sheet',
    ],
    'data': [
        'views/crm_phonecall.xml',
        'views/project.xml',
        'views/project_issue.xml',
        'menu_items.xml',
    ],
    'installable': True,
}
