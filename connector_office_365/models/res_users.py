# Copyright 2019 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models
from datetime import datetime
from urllib.parse import urlparse
import json

import logging
logger = logging.getLogger(__name__)
try:
    from requests_oauthlib.oauth2_session import OAuth2Session
except ImportError:
    logger.debug('Cannot import requests_oauthlib')

BASE_URL = 'https://login.microsoftonline.com/'
AUTH_URI = '/oauth2/v2.0/authorize'
TOKEN_URI = '/oauth2/v2.0/token'
API_BASE_URL = 'https://graph.microsoft.com/v1.0'


class Office365Error(Exception):
    """raised when an error is returned from an Office 365 API call"""
    def __init__(self, status, code, message):
        self.status = status
        self.code = code
        super().__init__(message)


class ResUsers(models.Model):
    _inherit = 'res.users'

    office_365_access_token = fields.Char()
    office_365_refresh_token = fields.Char()
    office_365_expiration = fields.Datetime()

    def __init__(self, pool, cr):
        super(ResUsers, self).__init__(pool, cr)
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend([
            'office_365_access_token',
            'office_365_refresh_token',
            'office_365_expiration'
        ])

        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend([
            'office_365_access_token',
            'office_365_refresh_token',
            'office_365_expiration'
        ])

    @api.multi
    def button_office_365_authenticate(self):
        self.ensure_one()

        url = self.office_365_authorization_url(
            [
                'User.Read',
                'Calendars.ReadWrite',
                'offline_access'
            ]
        )

        return {
            'name': 'OAuth',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'current',
            'url': url
        }

    @api.multi
    def button_office_365_test(self):
        self.ensure_one()
        res = self.office_365_get('/me/calendarview?StartDateTime=2017-01-01T00:00:00&EndDateTime=2020-01-01T00:00:00')
        return res

    @api.multi
    def _office_365_get_session(self, scope=None):
        self.ensure_one()
        config = self.env['ir.config_parameter'].sudo()
        client_id = config.get_param('office_365.client_id')
        redirect_uri = config.get_param('web.base.url') + '/office-365-oauth/success'

        token = None
        if self.office_365_access_token and self.office_365_expiration > fields.Datetime.now():
            token = {
                'access_token': self.office_365_access_token,
                'refresh_token': self.office_365_refresh_token,
                'token_type': 'Bearer'
            }

        return OAuth2Session(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            token=token
        )

    @api.model
    def office_365_authorization_url(self, scope=None):
        session = self._office_365_get_session(scope=scope)
        config = self.env['ir.config_parameter'].sudo()
        tenant_id = config.get_param('office_365.tenant_id')
        return session.authorization_url(
            url=BASE_URL + tenant_id + AUTH_URI
        )

    @api.model
    def office_365_get_token(self, authorization_response):
        config = self.env['ir.config_parameter'].sudo()
        client_secret = config.get_param('office_365.client_secret')
        tenant_id = config.get_param('office_365.tenant_id')

        session = self._office_365_get_session()
        return session.fetch_token(
            token_url=BASE_URL + tenant_id + TOKEN_URI,
            authorization_response=authorization_response,
            include_client_id=True,
            client_secret=client_secret
        )

    @api.multi
    def office_365_persist_token(self, token):
        self.ensure_one()

        expiration = datetime.fromtimestamp(token['expires_at'])

        self.write({
            'office_365_access_token': token['access_token'],
            'office_365_refresh_token': token['refresh_token'],
            'office_365_expiration': expiration
        })
        return token

    @api.multi
    def office_365_do_refresh_token(self):
        self.ensure_one()

        now = fields.Datetime.from_string(fields.Datetime.now())
        if self.office_365_expiration < now:
            session = self._office_365_get_session()

            config = self.env['ir.config_parameter'].sudo()
            tenant_id = config.get_param('office_365.tenant_id')
            client_id = config.get_param('office_365.client_id')
            client_secret = config.get_param('office_365.client_secret')

            token = session.refresh_token(
                token_url=BASE_URL + tenant_id + TOKEN_URI,
                client_id=client_id,
                client_secret=client_secret,
                refresh_token=self.office_365_refresh_token
            )
            return self.office_365_persist_token(token)
        return False

    @api.multi
    def office_365_request(self, method, url, data=None, headers=None):
        self.ensure_one()

        if not self.office_365_access_token:
            raise exceptions.UserError(
                _('User "{}" not authenticated with Office 365')
                .format(self.login)
            )

        config = self.env['ir.config_parameter'].sudo()
        client_id = config.get_param('office_365.client_id')
        client_secret = config.get_param('office_365.client_secret')

        # Refresh token
        self.office_365_do_refresh_token()

        session = self._office_365_get_session()

        url = urlparse(url).netloc and url or API_BASE_URL + url
        response = session.request(method, url,
                                   headers=headers,
                                   data=data,
                                   client_id=client_id,
                                   client_secret=client_secret)
        if not response.ok:
            error = json.loads(response.text)
            status = response.status_code
            error_code = error.get('error', {}).get('code')
            raise Office365Error(status, error_code, error['error']['message'])
        return response

    @api.multi
    def office_365_post(self, url, headers=None, data=None):
        return self.office_365_request('post', url, data, headers)

    @api.multi
    def office_365_get(self, url, headers=None):
        return self.office_365_request('get', url, headers=headers)

    @api.multi
    def office_365_patch(self, url, headers=None, data=None):
        return self.office_365_request('patch', url, data, headers)

    @api.multi
    def office_365_delete(self, url, headers=None, data=None):
        return self.office_365_request('delete', url, data, headers)
