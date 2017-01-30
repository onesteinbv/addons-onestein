# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.multi
    def unlink(self):
        if self.model in ['project.project', 'account.analytic.account']:
            self.env['mail.followers'].sudo().search(
                [('res_model', '=', self._name), ('res_id', 'in', self.ids)]
            ).unlink()
        return super(MailThread, self).unlink()
