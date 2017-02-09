# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os

from odoo.tests import common
from odoo.exceptions import Warning


class TestBaseDirectoryFilesDownload(common.TransactionCase):

    def test_01_create(self):
        dir = self.env['ir.filesystem.directory'].create({
            'name': 'Test Directory 1',
            'directory': '/tmp'
        })

        # test method get_dir()
        full_dir = dir.get_dir()
        self.assertEqual(full_dir[-1], '/')

        # test computed field file_ids
        self.assertGreaterEqual(len(dir.file_ids), 0)

        # test count list of directory
        self.assertEqual(len(dir.file_ids), dir.file_count)

        # test reload list of directory
        dir.reload()
        self.assertEqual(len(dir.file_ids), dir.file_count)

        # test files contained
        for file in dir.file_ids:
            filename = file.stored_filename
            directory = dir.get_dir()
            with open(os.path.join(directory, filename), 'rb') as f:
                content = f.read()
                self.assertEqual(file.file_content, content)

        # test onchange directory (to not existing)
        dir.directory = '/tpd'
        with self.assertRaises(Warning):
            dir.onchange_directory()
        self.assertEqual(len(dir.file_ids), 0)

    def test_02_copy(self):
        dir = self.env['ir.filesystem.directory'].create({
            'name': 'Test Orig',
            'directory': '/tmp'
        })

        # copy
        dir_copy = dir.copy()
        self.assertEqual(dir_copy.name, 'Test Orig (copy)')

    def test_03_not_existing_directory(self):
        dir = self.env['ir.filesystem.directory'].create({
            'name': 'Test Not Existing Directory',
            'directory': '/tpd'
        })
        self.assertEqual(len(dir.file_ids), 0)
        self.assertEqual(len(dir.file_ids), dir.file_count)

        # test onchange directory (to existing)
        dir.directory = '/tmp'
        self.assertGreaterEqual(len(dir.file_ids), 0)
        self.assertEqual(len(dir.file_ids), dir.file_count)
