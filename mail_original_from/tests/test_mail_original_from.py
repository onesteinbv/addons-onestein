# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import email

from odoo.tests import common
from odoo.tools import mute_logger


MAIL_MESSAGE = """Return-Path: <support@odoo-community.org>
To: info@odoo-community.org
Received: by mail1.openerp.com (Postfix, from userid 10002)
    id 5DF9ABFB2A; Fri, 10 Aug 2017 16:16:39 +0200 (CEST)
From: support@odoo-community.org
X-Original-From: info@odoo-community.org
Subject: {subject}
MIME-Version: 1.0
Content-Type: multipart/alternative;
    boundary="----=_Part_4200734_24778174.1344608186754"
Date: Fri, 10 Aug 2017 14:16:26 +0000
Message-ID: 123456789
------=_Part_4200734_24778174.1344608186754
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: quoted-printable

Please call me as soon as possible this afternoon!

--
Staff
------=_Part_4200734_24778174.1344608186754
Content-Type: text/html; charset=utf-8
Content-Transfer-Encoding: quoted-printable

<html>
 <head>=20
  <meta http-equiv=3D"Content-Type" content=3D"text/html; charset=3Dutf-8" />
 </head>=20
 <body style=3D"margin: 0; padding: 0; background: #ffffff;">=20

  <p>Please call me as soon as possible this afternoon!</p>

  <p>--<br/>
     Staff
  <p>
 </body>
</html>
------=_Part_4200734_24778174.1344608186754--
"""


class TestMailOriginalFrom(common.TransactionCase):

    @mute_logger('odoo.addons.mail.models.mail_thread')
    def test_01_message_parse(self):
        message = email.message_from_string(MAIL_MESSAGE)
        msg = self.env['mail.thread'].message_parse(message)
        self.assertIn(
            'From: support@odoo-community.org',
            MAIL_MESSAGE,
            'message_parse: missing From: support@odoo-community.org')
        self.assertIn(
            'X-Original-From: info@odoo-community.org',
            MAIL_MESSAGE,
            'message_parse: missing X-Original-From: info@odoo-community.org')
        self.assertEqual(msg['email_from'], 'info@odoo-community.org')
        self.assertEqual(msg['from'], 'info@odoo-community.org')

    @mute_logger('odoo.addons.mail.models.mail_thread')
    def test_02_message_route_verify(self):
        message = email.message_from_string(MAIL_MESSAGE)
        route = ('mail.mail', 1, None, self.env.uid, '')
        self.env['mail.thread'].message_route_verify(message, {}, route)
        self.assertIn(
            'From: info@odoo-community.org',
            message,
            'message_parse: missing From: info@odoo-community.org')
        self.assertIn(
            'X-Original-From: info@odoo-community.org',
            message,
            'message_parse: missing X-Original-From: info@odoo-community.org')
