# Copyright 2019 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def _office_365_from_event(self, event):
        values = super()._office_365_from_event(event)
        origin_leave_id = self.env.context.get('origin_leave_id')
        if origin_leave_id:
            leave = self.env['hr.leave'].browse(origin_leave_id)
            if leave.name:
                values = values.copy()
                values['subject'] = '{} - {}'.format(
                    values['subject'], leave.name
                )
        values['showAs'] = 'oof'
        return values

    @api.multi
    def unlink(self):
        if self.env.context.get('o365_override_user'):
            for obj in self:
                super(
                    CalendarEvent,
                    obj.with_context(user=obj.user_id)
                ).unlink()
        else:
            super().unlink()
