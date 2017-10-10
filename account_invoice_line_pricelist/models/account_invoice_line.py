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

        price_unit = self._common_recalc_price()
        if price_unit is not None and price_unit != 0:
            self.price_unit = price_unit

        return res

    def _common_recalc_price(self):
        """
        Re/calculate and return given price
        """
        if self.invoice_id.type not in ['out_invoice', 'out_refund']:
            return None

        partner = self.invoice_id.partner_id
        pricelist = self.invoice_id.pricelist_id
        product = self.product_id

        if not partner or not product or not pricelist:
            return None

        inv_date = self.invoice_id.date_invoice or date.today().strftime(DT)
        product = product.with_context(
            lang=partner.lang,
            partner=partner.id,
            quantity=self.quantity,
            date=inv_date,
            pricelist=pricelist.id,
            uom=self.uom_id.id
        )

        return self.env['account.tax']._fix_tax_included_price(
            product.price,
            product.taxes_id,
            self.invoice_line_tax_ids
        )

    def create(self, vals):
        """
        Update price if missing, after real create()
        """
        line = super(AccountInvoiceLine, self).create(vals)
        if line.invoice_id:
            invoice = line.invoice_id
            if ((not line.price_unit) or line.price_unit == 0) and (invoice.pricelist_id and invoice.pricelist_id.id):
                price_unit = line._common_recalc_price()
                if price_unit is not None and price_unit != 0:
                    line.price_unit = price_unit    #triggers write()
        return line

    @api.multi
    def write(self, vals):
        """
        Update price whenever missing, before real write()
        Remember: do *not* update rec.price_unit directly! that triggers write()
        """
        for rec in self:
            if (rec.invoice_id.pricelist_id and rec.invoice_id.pricelist_id.id):
                if 'price_unit' in vals and vals['price_unit'] is None or vals['price_unit'] == 0:
                    #INSERT/UPDATE price_unit
                    price_unit = rec._common_recalc_price()
                    if price_unit is not None:
                        vals['price_unit'] = price_unit
                else:
                    #UPDATE record
                    if rec.price_unit is None or rec.price_unit == 0:
                        price_unit = rec._common_recalc_price()
                        if price_unit is not None and price_unit != 0:
                            vals['price_unit'] = price_unit
        return super(AccountInvoiceLine, self).write(vals)
