from odoo.tests.common import SavepointCase
from datetime import datetime, timedelta

import responses
import uuid
import json
import re


class TestAdminDeleteLeaves(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env['res.users'].with_context(
            tracking_disable=True
        ).create({
            'name': 'Max Mustermann',
            'login': 'MMn'
        })
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Max Mustermann',
            'user_id': cls.user.id,
        })

        alloc = cls.env['hr.leave.allocation'].create({
            'employee_id': cls.employee.id,
            'number_of_days': 10,
        })
        alloc.action_approve()

    @responses.activate
    def test_can_delete_leave(self):
        token = {}
        token['access_token'] = str(uuid.uuid4())
        token['refresh_token'] = str(uuid.uuid4())
        token['expires_at'] = (datetime.now() + timedelta(days=1)).timestamp()

        responses.add(
            responses.POST,
            'https://login.microsoftonline.com/common/oauth2/v2.0/token',
            body=json.dumps(token), status=200, content_type='application/json'
        )

        event_create = {
            'id': str(uuid.uuid4()),
            'webLink': 'http://blubb.local'}
        responses.add(
            responses.POST,
            'https://graph.microsoft.com/v1.0/me/events/',
            body=json.dumps(event_create),
            status=200,
            content_type='application/json'
        )
        responses.add(
            responses.PATCH,
            re.compile('https://graph.microsoft.com/v1.0/me/events/[0-9-]*'),
            body='',
            status=200,
            content_type='application/json'
        )
        responses.add(
            responses.DELETE,
            re.compile('https://graph.microsoft.com/v1.0/me/events/[0-9-]*'),
            body='',
            status=200,
            content_type='application/json'
        )

        token = self.user.office_365_get_token(
            'https://blubb.local?code=329293&access_token=348484'
        )
        self.user.office_365_persist_token(token)
        self.leave = self.env['hr.leave'].create({
            'employee_id': self.employee.id,
            'date_from': datetime.now() + timedelta(days=1),
            'date_to': datetime.now() + timedelta(days=2),
            'number_of_days': 1,
        })
        self.leave.action_approve()
        # we don't want to get a usererror here
        self.assertEqual(len(self.leave.meeting_id), 1)
        self.leave.action_refuse()
        self.assertEqual(len(self.leave.meeting_id), 0)
        self.assertEqual(self.leave.state, 'refuse')
