# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Disable LDAP referrals',
    'images': [],
    'version': '9.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ONESTEiN BV',
    'website': 'http://www.onestein.eu',
    'category': 'Authentication',
    'depends': ['auth_ldap'],
    'installable': True,
    'external_dependencies': {
        'python': ['ldap'],
    }
}
