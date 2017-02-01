# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def _auto_end(self):
        table = self._table[0:6]
        if table != 'x_bve_':
            super(Base, self)._auto_end()

    @api.model
    def _setup_complete(self):
        name = self._name[0:6]
        if name != 'x_bve.':
            super(Base, self)._setup_complete()
