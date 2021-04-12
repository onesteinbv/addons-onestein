# Copyright 2021 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def office_365_persist_token(self, token):
        tok = super().office_365_persist_token(token)
        self._async_office_365_push_events()
        return tok

    def _async_office_365_push_events(self):
        self.ensure_one()
        try:
            leaves = self.env['hr.leave'].search(
                [
                    ('need_o365_manual_push', '=', True),
                    ('user_id', '=', self.id),
                ]
            )
            if leaves:
                _logger.info('Pushing pending validated leaves to office365: %s', leaves)
            for leave in leaves:
                leave.office_365_manual_push()
        except Exception:
            _logger.exception('unable to push pending validated leaves')
            # ignore for now, will be retried later
        try:
            # delete pending meetings from canceled leaves
            leaves = self.env['hr.leave'].search(
                [('state', 'in', ('draft', 'cancel')),
                 ('meeting_id', '!=', False),
                 ]
            )
            if leaves:
                _logger.info('Removing calendar events of refused leaves from Office365', leaves)
            leaves.with_context(o365_override_user=True).mapped('meeting_id').unlink()
        except Exception:
            _logger.exception('unable to remove refused leaves events')
            # ignore for now, will be retried later
