# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def _auto_end(self):
        name = self._table[0:6]
        if name != 'x_bve.':
            super(Base, self)._auto_end()
