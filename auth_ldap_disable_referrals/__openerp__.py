# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Disable LDAP referrals',
    'images': [],
    'version': '8.0.1.0.0',
    'author': 'ONESTEiN BV',
    'website': 'http://www.onestein.eu',
    'category': 'Authentication',
    'depends': ['auth_ldap'],
    'data': [],
    'auto_install': False,
    'installable': True,
    'external_dependencies': {
        'python' : ['ldap'],
    }
}
