# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Project Analytic Align Follower',
    'summary': 'Sync Followers of Analytic Account and Project',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'version': '10.0.1.0.0',
    'depends': [
        'analytic',
        'project',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
}
