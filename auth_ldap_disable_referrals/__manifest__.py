# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Disable LDAP referrals',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Authentication',
    'depends': ['auth_ldap'],
    'installable': True,
    'external_dependencies': {
        'python': ['ldap'],
    }
}
