# Copyright 2019 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
import re
from dateutil import parser
from datetime import timedelta

from odoo import _, api, fields, models, exceptions


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    office_365_series_id = fields.Char()
    office_365_id = fields.Char()
    office_365_url = fields.Char()

    @api.model
    def _office_365_to_event(self, event):
        user = self.env.context.get('user', self.env.user)
        start = parser.parse(event['start']['dateTime'])
        stop = parser.parse(event['end']['dateTime'])

        description = event['body']['content']
        if event['body']['contentType'] == 'html':
            description = re.sub('<[^>]+>', '', description)

        if event['isAllDay']:
            stop -= timedelta(days=1)

        return {
            'name': event['subject'],
            'privacy': 'private',
            'state': 'open',
            'allday': event['isAllDay'],
            'user_id': event['isOrganizer'] and user.id,
            'show_as': event['showAs'],
            'office_365_url': event['webLink'],
            'office_365_id': event['id'],
            'office_365_series_id': event.get('seriesMasterId', False),
            'description': description,
            'start': start,
            'stop': stop
        }

    @api.model
    def _office_365_from_event(self, event):
        end = event.stop
        start = event.start

        # The Event.End property for an all-day event needs to be set to midnight
        if event.allday:
            end += timedelta(seconds=1)

        return {
            'body': {
                'contentType': 'text',
                'content': event.description
            },
            'end': {
                'dateTime': fields.Datetime.to_string(end),
                'timeZone': 'utc'
            },
            'start': {
                'dateTime': fields.Datetime.to_string(start),
                'timeZone': 'utc'
            },
            'isAllDay': event.allday,
            'showAs': event.show_as,
            'subject': event.name,

        }

    @api.model
    def office_365_fetch(self, start, end):
        user = self.env.context.get('user', self.env.user)

        if not user.office_365_access_token:
            return user.button_office_365_authenticate()
        headers = {
            'Prefer': 'odata.track-changes;outlook.timezone="UTC"',
        }
        url = '/me/calendarview?StartDateTime={}&EndDateTime={}'.format(
            start, end
        )
        result = json.loads(user.office_365_get(
            url,
            headers=headers
        ).text)
        self._office_365_process_changes(result['value'], start, end)

    def _office_365_process_changes(self, changes, start, end):
        series = {}
        user = self.env.context.get('user', self.env.user)
        self = self.with_context(office_365_force=True)

        ids = []
        for change in changes:
            existing = self.search([
                '|',
                ('office_365_id', '=', change['id']),
                ('office_365_series_id', '=', change['id'])
            ])

            if change['type'] in ('singleInstance', 'exception'):
                values = self._office_365_to_event(change)
                if existing:
                    existing.write(values)
                else:
                    self.create(values)
            elif change['type'] == 'seriesMaster':
                series[change['id']] = change
            elif change['type'] == 'occurrence':
                occurrence = series[change['seriesMasterId']].copy()
                occurrence['id'] = change['id']
                occurrence['start'] = change['start']
                occurrence['end'] = change['end']
                occurrence['seriesMasterId'] = change['seriesMasterId']
                values = self._office_365_to_event(occurrence)
                if existing:
                    existing.write(values)
                else:
                    self.create(values)
            ids.append(change['id'])

        to_delete = self.search([
            ('office_365_id', 'not in', ids),
            ('user_id', '=', user.id),
            ('start', '<', end),
            ('stop', '>', start)
        ])
        to_delete.unlink()

    @api.multi
    def office_365_open(self):
        self.ensure_one()
        return {
            'name': 'Open in Office 365',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'current',
            'url': self.office_365_url
        }

    @api.multi
    def write(self, vals):
        res = super(CalendarEvent, self).write(vals)
        user = self.env.context.get('user', self.env.user)
        for event in self:
            if event.office_365_id and not \
                    self.env.context.get('office_365_force', False):
                if event.user_id.id != user.id:
                    raise exceptions.UserError(
                        _('You are not the organizer of this '
                          'event please try to edit this event in Office 365.')
                    )

                user.office_365_patch(
                    '/me/events/{}'.format(event.office_365_id),
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(self._office_365_from_event(event))
                )
        return res

    @api.multi
    def unlink(self):
        user = self.env.context.get('user', self.env.user)
        for event in self:
            if event.office_365_id and not self.env.context.get('office_365_force', False):
                if event.user_id.id != user.id:
                    raise exceptions.UserError(
                        _('You are not the organizer of this '
                          'event please try delete this event in Office 365.')
                    )

                user.office_365_delete(
                    '/me/events/{}'.format(event.office_365_id),
                )

        return super(CalendarEvent, self).unlink()
