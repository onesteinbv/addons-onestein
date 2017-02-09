# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from os import listdir
from os.path import isfile, join, exists
from odoo import api, fields, models, _
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class IrFilesystemDirectory(models.Model):
    _name = 'ir.filesystem.directory'
    _description = 'Filesystem Directory'

    name = fields.Char(required=True, copy=False)
    directory = fields.Char()
    file_ids = fields.One2many(
        'ir.filesystem.file',
        compute='_compute_file_ids',
        string='Files'
    )
    file_count = fields.Integer(compute='_file_count', string="# Files")

    @api.multi
    def get_dir(self):
        self.ensure_one()
        dir = self.directory
        if dir and dir[-1] != '/':
            dir += '/'
        return dir

    @api.multi
    def _compute_file_ids(self):
        File = self.env['ir.filesystem.file']
        for dir in self:
            dir.file_ids = None
            if dir.get_dir():
                for file in dir._get_directory_files():
                    dir.file_ids += File.create({
                        'name': file,
                        'filename': file,
                        'stored_filename': file,
                        'directory_id': dir.id,
                    })

    @api.onchange('directory')
    def onchange_directory(self):
        if self.directory and not exists(self.directory):
            raise Warning(_('Directory does not exist'))

    @api.multi
    def _file_count(self):
        for directory in self:
            directory.file_count = len(directory.file_ids)

    @api.multi
    def _get_directory_files(self):

        def get_files(directory, files):
            for file in listdir(directory):
                if isfile(join(directory, file)) and file[0] != '.':
                    files.append(file)

        self.ensure_one()
        files = []
        if self.get_dir() and exists(self.get_dir()):
            try:
                get_files(self.get_dir(), files)
            except (IOError, OSError):
                _logger.info(
                    "_get_directory_files reading %s",
                    self.get_dir(),
                    exc_info=True
                )
        return files

    @api.multi
    def reload(self):
        self.onchange_directory()

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {}, name=_("%s (copy)") % self.name)
        return super(IrFilesystemDirectory, self).copy(default=default)
