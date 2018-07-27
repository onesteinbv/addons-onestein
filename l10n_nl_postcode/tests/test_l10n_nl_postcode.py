# Copyright 2017-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.tools.translate import _


class TestL10NNLPostcode(common.TransactionCase):
    def setUp(self):
        super(TestL10NNLPostcode, self).setUp()
        self.partner = self.env.ref('base.res_partner_3')

    def test_01_onchange_with_non_blocking_warning(self):
        self.partner.write({
            'country_id': self.env.ref('base.nl').id,
            'zip': '80021',
        })

        warning = self.partner.onchange_zip_l10n_nl_postcode()
        msg = _('The Postcode you entered (%s) is not valid.')
        tst_warning = {'warning': {
            'title': _('Warning!'),
            'message': msg % '80021',
        }}
        self.assertTrue(warning)
        self.assertEqual(warning, tst_warning)
        # zip didn't change
        self.assertEqual(self.partner.zip, '80021')

    def test_02_onchange_no_country(self):
        self.partner.write({
            'zip': '4813LE',
        })
        res = self.partner.onchange_zip_l10n_nl_postcode()
        self.assertFalse(res)
        # zip didn't change
        self.assertEqual(self.partner.zip, '4813LE')

    def test_03_onchange_other_country(self):
        self.partner.write({
            'country_id': self.env.ref('base.be').id,
            'zip': '4813LE',
        })
        res = self.partner.onchange_zip_l10n_nl_postcode()
        self.assertFalse(res)
        # zip didn't change
        self.assertEqual(self.partner.zip, '4813LE')

    def test_04_onchange_format(self):
        self.partner.write({
            'country_id': self.env.ref('base.nl').id,
            'zip': '4813LE',
        })
        res = self.partner.onchange_zip_l10n_nl_postcode()
        self.assertFalse(res)
        # zip formatted
        self.assertEqual(self.partner.zip, '4813 LE')

    def test_05_onchange_format(self):
        self.partner.write({
            'country_id': self.env.ref('base.nl').id,
            'zip': '4813 le',
        })
        res = self.partner.onchange_zip_l10n_nl_postcode()
        self.assertFalse(res)
        # zip formatted
        self.assertEqual(self.partner.zip, '4813 LE')

    def test_06_skip_onchange(self):
        self.partner.write({
            'country_id': self.env.ref('base.nl').id,
            'zip': '4813 le',
        })
        res = self.partner.with_context(
            skip_postcode_check=True
        ).onchange_zip_l10n_nl_postcode()
        self.assertFalse(res)
        # zip didn't change
        self.assertEqual(self.partner.zip, '4813 le')
