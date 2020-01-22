# Copyright 2019 Onestein
# Copyright 2019 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
import json
import re
from dateutil import parser
from datetime import timedelta

from odoo import _, api, fields, models, exceptions
from .res_users import Office365Error

_logger = logging.getLogger(__name__)


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

        show_as_options = [sel[0] for sel in self._fields['show_as'].selection]
        show_as = (
            event['showAs'] if event['showAs'] in show_as_options else 'busy'
        )

        return {
            'name': event['subject'],
            'privacy': 'private',
            'state': 'open',
            'allday': event['isAllDay'],
            'user_id': event['isOrganizer'] and user.id,
            'show_as': show_as,
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

        values = {
            'body': {
                'contentType': 'text',
                'content': event.description or '',
            },
            'isAllDay': event.allday,
            'showAs': event.show_as,
            'subject': event.name,
        }

        if event.allday:
            # The Event.End property for an all-day event needs to be set to
            # midnight
            start = start.date()
            end = end.date()
            # for all day events, we have to set the next day (for instance if
            # start day is 21-06-2019, the end is 22-06-2019 for a one-day
            # event)
            end += timedelta(days=1)
            # if we don't use a real TZ, the all day events are buggy
            # and display an extra day on o365's calendar
            values.update({
                'end': {
                    'dateTime': fields.Date.to_string(end),
                    'timeZone': self.user_id.tz or 'utc'
                },
                'start': {
                    'dateTime': fields.Date.to_string(start),
                    'timeZone': self.user_id.tz or 'utc'
                },
            })

        else:
            values.update({
                'end': {
                    'dateTime': fields.Datetime.to_string(end),
                    'timeZone': 'utc'
                },
                'start': {
                    'dateTime': fields.Datetime.to_string(start),
                    'timeZone': 'utc'
                },
            })

        return values

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

    def _office_365_push_create(self):
        if not self.user_id:
            return
        _logger.debug('post event %s', self.name)
        result = self.user_id.office_365_post(
            '/me/events/',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(self._office_365_from_event(self))
        )
        o365_event = result.json()
        self.write({
            'office_365_id': o365_event['id'],
            'office_365_series_id': o365_event.get('seriesMasterId'),
            'office_365_url': o365_event['webLink'],
        })

    def _office_365_push_update(self):
        _logger.debug('patch event %s', self.name)
        self.env.user.office_365_patch(
            '/me/events/{}'.format(self.office_365_id),
            headers={'Content-Type': 'application/json'},
            data=json.dumps(self._office_365_from_event(self))
        )

    @api.multi
    def office_365_push(self):
        for record in self:
            if not record.office_365_id:
                record._office_365_push_create()
            else:
                if record.user_id.id != self.env.user.id:
                    raise exceptions.UserError(
                        _('You are not the organizer of the event "{}"'
                          ' please try to edit this event in Office 365.')
                        .format(record.name)
                    )
                record._office_365_push_update()

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
            ('office_365_id', '!=', False),
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

    @api.model_create_multi
    def create(self, vals_list):
        records = super(CalendarEvent, self).create(vals_list)
        if not self.env.context.get('office_365_force'):
            records.office_365_push()
        return records

    @api.multi
    def write(self, vals):
        res = super(CalendarEvent, self).write(vals)
        user = self.env.context.get('user', self.env.user)
        for event in self:
            if event.office_365_id and not \
                    self.env.context.get('office_365_force', False):
                if user != self.env.user:
                    event = event.sudo(user)
                event.office_365_push()
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
                try:
                    user.office_365_delete(
                        '/me/events/{}'.format(event.office_365_id),
                    )
                except Office365Error as exc:
                    if exc.code == 'ErrorItemNotFound':
                        # don't block suppressing the calendar event in Odoo if
                        # the event cannot be found in Office365 (this can
                        # happen if it was manually deleted in Office365)
                        _logger.info(
                            "The event related to Odoo record %s "
                            "in Office was not found: %s",
                            event, exc
                        )
                    else:
                        raise
        return super(CalendarEvent, self).unlink()
