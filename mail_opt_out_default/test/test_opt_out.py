# -*- coding: utf-8 -*-
# © 2015 Salton Massally <smassally@idtlabs.sl>
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestOptOut(common.TransactionCase):

    def setUp(self):
        super(TestOptOut, self).setUp()
        self.company = self.env.ref('base.main_company')

    def test_company_default_values(self):
        # test loading of default company values
        self.assertTrue(self.company.default_opt_out == True)

    def test_configuration_default_values(self):
        # test loading of default configuration values
        config_model = self.env['base.config.settings']
        config = config_model.create({})
        self.assertTrue(config.default_opt_out == True)

    def test_partner_default_values(self):
        # test loading of default partner values
        new_partner = self.env['res.partner'].create({
            'name': 'New Test Partner'
        })
        self.assertTrue(new_partner.opt_out == True)
