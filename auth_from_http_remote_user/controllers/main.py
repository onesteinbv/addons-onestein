# -*- coding: utf-8 -*-
# Copyright 2014 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import random
import logging
import werkzeug

from odoo import http, SUPERUSER_ID
from odoo.api import Environment
from odoo.http import request
from odoo.addons.web.controllers import main
from odoo.modules.registry import RegistryManager
from ..models.auth_from_http_remote_user import \
    AuthFromHttpRemoteUserInstalled
from .. import utils

_logger = logging.getLogger(__name__)


class Home(main.Home):

    _REMOTE_USER_ATTRIBUTE = 'HTTP_REMOTE_USER'

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        main.ensure_db()
        try:
            self._bind_http_remote_user(http.request.session.db)
        except http.AuthenticationError:
            return werkzeug.exceptions.Unauthorized().get_response()
        return super(Home, self).web_client(s_action, **kw)

    def _search_user(self, res_users, login):
        users = res_users.search([
            ('login', '=', login),
            ('active', '=', True)])
        assert len(users) < 2
        if users:
            return users[0]
        return None

    def _bind_http_remote_user(self, db_name):
        try:
            registry = RegistryManager.get(db_name)
            with registry.cursor() as cr:
                if AuthFromHttpRemoteUserInstalled._name not in registry:
                    # module not installed in database,
                    # continue usual behavior
                    return

                headers = http.request.httprequest.headers.environ

                login = headers.get(self._REMOTE_USER_ATTRIBUTE, None)
                if not login:
                    # no HTTP_REMOTE_USER header,
                    # continue usual behavior
                    _logger.debug("Required fields '%s' not found in http"
                                  " headers\n %s",
                                  self._REMOTE_USER_ATTRIBUTE, headers)
                    return

                request_login = request.session.login
                if request_login:
                    if request_login == login:
                        # already authenticated
                        return
                    else:
                        request.session.logout(keep_db=True)

                env = Environment(cr, SUPERUSER_ID, {})
                res_users = env['res.users']
                user = self._search_user(res_users, login)
                if not user:
                    # HTTP_REMOTE_USER login not found in database
                    request.session.logout(keep_db=True)
                    raise http.AuthenticationError()

                # generate a specific key for authentication
                key = randomString(utils.KEY_LENGTH, '0123456789abcdef')
                user.write({'sso_key': key})
            request.session.authenticate(db_name, login=login,
                                         password=key, uid=user.id)
        except http.AuthenticationError, e:
            raise e
        except Exception, e:
            _logger.error("Error binding Http Remote User session",
                          exc_info=True)
            raise e


randrange = random.SystemRandom().randrange


def randomString(length, chrs):
    """Produce a string of length random bytes, chosen from chrs."""
    n = len(chrs)
    return ''.join([chrs[randrange(n)] for _ in xrange(length)])
