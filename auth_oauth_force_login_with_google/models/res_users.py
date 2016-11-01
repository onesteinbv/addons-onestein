# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import api, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @classmethod
    def _login(cls, db, login, password):
        if not password:
            return False
        try:
            with cls.pool.cursor() as cr:
                self = api.Environment(cr, SUPERUSER_ID, {})[cls._name]
                res = self.env['res.users'].sudo().search([
                    ('login', '=', login)
                ], limit=1)
                if res:
                    user_id = res.id
                    if user_id == SUPERUSER_ID:
                        return super(ResUsers, cls)._login(
                            db, login, password
                        )

        except AccessDenied:
            _logger.info("Login failed for db:%s login:%s", db, login)

        return False
