# -*- coding: utf-8 -*-
# Copyright 2014 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
import mock
import os
from contextlib import contextmanager
import unittest


@contextmanager
def mock_cursor(cr):
    with mock.patch('odoo.sql_db.Connection.cursor') as mocked_cursor_call:
        org_close = cr.close
        org_autocommit = cr.autocommit
        try:
            cr.close = mock.Mock()
            cr.autocommit = mock.Mock()
            mocked_cursor_call.return_value = cr
            yield
        finally:
            cr.close = org_close
    cr.autocommit = org_autocommit


class TestResUsers(common.TransactionCase):

    def test_login(self):
        ResUsers = self.registry('res.users')
        res = ResUsers.authenticate(
            common.get_db_name(), 'admin', 'admin', None)
        uid = res
        self.assertTrue(res, "Basic login must works as expected")
        token = "123456"
        res = ResUsers.authenticate(
            common.get_db_name(), 'admin', token, None)
        self.assertFalse(res)
        # mimic what the new controller do when it find a value in
        # the http header (HTTP_REMODE_USER)
        ResUsers.browse(uid).write({'sso_key': token})

        # Here we need to mock the cursor since the login is natively done
        # inside its own connection
        with mock_cursor(self.cr):
            # We can verifies that the given (uid, token) is authorized for
            # the database
            ResUsers.check(common.get_db_name(), uid, token)

            # we are able to login with the new token
            res = ResUsers.authenticate(
                common.get_db_name(), 'admin', token, None)
            self.assertTrue(res)

    @unittest.skipIf(os.environ.get('TRAVIS'),
                     'When run by travis, tests runs on a database with all '
                     'required addons from server-tools and their dependencies'
                     ' installed. Even if `auth_from_http_remote_user` does '
                     'not require the `mail` module, The previous installation'
                     ' of the mail module has created the column '
                     '`notification_email_send` as REQUIRED into the table '
                     'res_partner. BTW, it\'s no more possible to copy a '
                     'res_user without an intefirty error')
    def test_copy(self):
        '''Check that the sso_key is not copied on copy
        '''
        vals = {'sso_key': '123'}
        self.user.write(vals)
        read_vals = self.user.read(['sso_key'])
        self.assertDictContainsSubset(vals, read_vals)
        copy = self.user.copy()
        read_vals = copy.read(['sso_key'])
        self.assertFalse(read_vals.get('sso_key'))
