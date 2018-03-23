# Copyright 2017-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

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

    def test_02_onchange(self):
        values = {
            'zip': '80021',
        }

        field_onchange = self.Partner._onchange_spec()
        self.assertEqual(field_onchange.get('zip'), '1')

        # workaround to avoid _compute_sale_order_count() being called
        # since self.read(['child_ids']) will raise an access right error
        to_remove_fields = [
            'sale_order_count',
            'purchase_order_count',
            'supplier_invoice_count'
        ]
        for to_remove in to_remove_fields:
            if to_remove in field_onchange.keys():
                del field_onchange[to_remove]

        self.Partner.onchange(values, 'zip', field_onchange)
        self.Partner.with_context(skip_postcode_check=True).onchange(
            values, 'zip', field_onchange)
