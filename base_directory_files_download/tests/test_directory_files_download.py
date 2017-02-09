# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


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
