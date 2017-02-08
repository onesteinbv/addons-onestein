# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp import api, fields, models, _
from openerp.exceptions import Warning

_logger = logging.getLogger(__name__)


class IrFilesystemDirectory(models.Model):
    _inherit = 'ir.filesystem.directory'

    is_backup = fields.Boolean()

    @api.multi
    def get_dir(self):
        if self.is_backup:
            backup = self.env['db.backup'].search([], limit=1)
            if not backup:
                raise Warning(_(
                    '''No backup configuration.'''))
            self.directory = backup.folder
        return super(IrFilesystemDirectory, self).get_dir()
