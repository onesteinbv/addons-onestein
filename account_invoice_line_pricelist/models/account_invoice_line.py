# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from datetime import date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DT


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(AccountInvoiceLine, self)._onchange_product_id()

        if self.invoice_id.type not in ['out_invoice', 'out_refund']:
            return res

        partner = self.invoice_id.partner_id
        pricelist = self.invoice_id.pricelist_id
        product = self.product_id

        if not partner or not product or not pricelist:
            return res

        product = product.with_context(
            lang=partner.lang,
            partner=partner.id,
            quantity=self.quantity,
            date=self.invoice_id.date_invoice,
            pricelist=pricelist.id,
            uom=self.uom_id.id
        )

        inv_date = self.invoice_id.date_invoice or date.today().strftime(DT)
        self.price_unit = self.env['account.tax'].with_context(
            date=inv_date)._fix_tax_included_price(
            product.price,
            product.taxes_id,
            self.invoice_line_tax_ids
        )
        return res
