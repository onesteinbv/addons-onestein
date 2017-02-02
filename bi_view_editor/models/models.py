# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def _not_bi_view(self):
        if self._name[0:6] != 'x_bve.':
            return True
        return False

    @api.model
    def _auto_end(self):
        if self._not_bi_view():
            super(Base, self)._auto_end()

    @api.model
    def _setup_complete(self):
        if self._not_bi_view():
            super(Base, self)._setup_complete()

    @api.model
    def _read_group_process_groupby(self, gb, query):
        if self._not_bi_view():
            return super(Base, self)._read_group_process_groupby(gb, query)

        split = gb.split(':')
        if split[0] not in self._fields:
            raise UserError(
                _('No data to be displayed.'))
        return super(Base, self)._read_group_process_groupby(gb, query)
