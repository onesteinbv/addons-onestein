# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Base(models.AbstractModel):
    _inherit = 'base'

    def _register_hook(self):
        res = super(Base, self)._register_hook()
        name = self._name[0:6]
        if name == 'x_bve.':
            return self.sudo()._patch_methods()

        return res

    @api.multi
    def _patch_methods(self):
        updated = False
        model_model = self.env[self._name]
        if model_model._log_access:
            model_model._log_access = False
            updated = True

        return updated
