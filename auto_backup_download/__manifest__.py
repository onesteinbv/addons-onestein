# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Database Auto-Backup Download',
    'summary': 'Download the backup files of your database',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Tools',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'base_setup',
        'base_directory_file_download',
        'auto_backup',
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/backup_directory.xml',
        'views/ir_filesystem_directory.xml',
    ],
    'installable': True,
}
