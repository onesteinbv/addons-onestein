# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class WizardIrModelMenuCreate(models.TransientModel):
    _inherit = 'wizard.ir.model.menu.create'

    @api.multi
    def menu_create(self):
        if self._context.get('active_model') == 'bve.view':
            active_id = self._context.get('active_id')
            bve_view = self.env['bve.view'].browse(active_id)
            menu = self.env['ir.ui.menu'].create({
                'name': bve_view.name,
                'parent_id': self.menu_id.id,
                'action': 'ir.actions.act_window,%d' % (bve_view.action_id,)
            })
            self.env['ir.model.data'].create({
                'name': bve_view.name,
                'noupdate': True,
                'module': 'bi_view_editor',
                'model': 'ir.ui.menu',
                'res_id': menu.id,
            })
            return {'type': 'ir.actions.act_window_close'}
        return super(WizardIrModelMenuCreate, self).menu_create()
