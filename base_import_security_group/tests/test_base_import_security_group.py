# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (http://www.onestein.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.tests import common, HttpCase
from odoo.tools import mute_logger


class TestImportSecurityGroup(common.TransactionCase):
    def setUp(self):
        super(TestImportSecurityGroup, self).setUp()
        self.Access = self.env['ir.model.access']
        self.user_test = self.env.ref('base.user_demo')
        self.group_ref = 'base_import_security_group.group_import_csv'
        self.group = self.env.ref(self.group_ref)

    def test_01_load(self):

        fields = (
            'id',
            'name',
            'perm_read',
            'perm_write',
            'perm_create',
            'perm_unlink',
        )

        data = [
            ('access_res_users_test', 'res.users test', '1', '0', '0', '0',),
            ('access_res_users_test2', 'res.users test2', '1', '1', '1', '1'),
        ]

        res = self.Access.load(fields, data)

        self.assertEqual(res['ids'], False)
        self.assertEqual(len(res['messages']), 2)
        self.assertEqual(
            res['messages'][0]['message'],
            "Missing required value for the field 'Object' (model_id)")
        self.assertEqual(
            res['messages'][1]['message'],
            "Missing required value for the field 'Object' (model_id)")

        res2 = self.Access.sudo(self.user_test).load(fields, data)

        self.assertEqual(res2['ids'], None)
        self.assertEqual(len(res2['messages']), 1)
        self.assertEqual(
            res2['messages'][0]['message'],
            'User (ID: %s) is not allowed to import data in '
            'model ir.model.access.' % self.user_test.id)

@common.at_install(False)
@common.post_install(True)
class TestImportSecurityGroupHTTP(HttpCase):
    def setUp(self):
        super(TestImportSecurityGroupHTTP, self).setUp()
        self.user_test = self.env.ref('base.user_demo')
        self.group_ref = 'base_import_security_group.group_import_csv'
        self.group = self.env.ref(self.group_ref)

    def test_02_in_group(self):
        self.env.user.groups_id += self.group
        self.assertTrue(self.env.user.has_group(self.group_ref))
        self.has_button_import()

    def test_03_not_in_group(self):
        self.env.user.groups_id -= self.group
        self.assertFalse(self.env.user.has_group(self.group_ref))
        self.has_button_import(falsify=True)

    def has_button_import(self, falsify=False):
        """
         Verify that the button is either visible or invisible.
         After the adjacent button is loaded, allow for a second for
         the asynchronous call to finish and update the visibility """
        code = """
            if (%s$('.o_button_import').is(':visible')) {
                console.log('ok');
            } else {
                console.log('error');
            };
        """ % ('!' if falsify else '')
        link = '/web#action=%s' % self.env.ref('base.action_res_users').id

        # with mute_logger('openerp.addons.base.res.res_users'):
        # Mute debug log about failing row lock upon user login
        self.phantom_js(
            link, code, "$('button.o_list_button_add').length",
            login=self.env.user.login)
