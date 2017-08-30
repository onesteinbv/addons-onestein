# -*- coding: utf-8 -*-
# © 2014-2016 Camptocamp SA (Damien Crier)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common
from openerp import fields, tools
from openerp.modules import get_module_resource


class TestAccountCostSpread(common.TransactionCase):

    def setUp(self):
        super(TestAccountCostSpread, self).setUp()
        #using the minimal test XML from account 9.0, data valid for 8.0 too
        tools.convert_file(self.cr, 'account',
                           get_module_resource('account_cost_spread', 'tests',
                                               'account_minimal_test.xml'),
                           {}, 'init', False, 'test')
        # create invoice and confirm
        #create spread

    def test_spread(self):
        # change spreadlines
        # create moves for reconciliable accounts
        # create moves for reconciliable accounts
