# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.account_cost_spread.tests.test_code_spread \
    import TestAccountCostSpread


class TestAccountCostSpreadAll(TestAccountCostSpread):

    def test_01_create_all_moves(self):
        # spread date set
        self.invoice_line.write({
            'period_number': 12,
            'period_type': 'month',
            'spread_date': '2017-02-01'
        })

        # change the state of invoice to open by clicking Validate button
        self.invoice.action_invoice_open()
        self.assertEqual(len(self.invoice_line.spread_line_ids), 12)

        # create moves for all the spread lines
        self.invoice_line.create_all_moves()

        for spread_line in self.invoice_line.spread_line_ids:
            self.assertEqual(len(spread_line.move_id), 1)
