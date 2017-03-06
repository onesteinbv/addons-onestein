# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.tools.translate import _


class TestL10NNLPostcode(common.TransactionCase):
    def setUp(self):
        super(TestL10NNLPostcode, self).setUp()
        self.Partner = self.env['res.partner']

        self.partner_1 = self.env.ref('base.res_partner_2')
        self.partner_2 = self.env.ref('base.res_partner_3')

    def test_01_onchange(self):
        values = {
            'zip': '80021',
        }

        field_onchange = self.partner_1._onchange_spec()
        self.assertEqual(field_onchange.get('zip'), '1')

        self.partner_1.onchange(values, 'zip', field_onchange)
        self.partner_1.with_context(skip_postcode_check=True).onchange(
            values, 'zip', field_onchange)

        self.partner_2.write({
            'country_id': self.env.ref('base.nl').id,
            'zip': values['zip'],
        })

        warning = self.partner_2.onchange_zip_l10n_nl_postcode()
        msg = _('The Postcode you entered (%s) is not valid.')
        tst_warning = {'warning': {
            'title': _('Warning!'),
            'message': msg % values['zip'],
        }}
        self.assertEqual(warning, tst_warning)

        self.partner_2.write({
            'zip': '4813LE',
        })
        self.partner_2.onchange_zip_l10n_nl_postcode()
