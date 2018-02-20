# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def product_id_change(
            self, product, uom_id, qty=0, name='', type='out_invoice',
            partner_id=False, fposition_id=False, price_unit=False,
            currency_id=False, company_id=None):
        res = super(AccountInvoiceLine, self).product_id_change(
            product, uom_id, qty=qty, name=name, type=type,
            partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id,
            company_id=company_id)
        if not res or not res['value']:
            return res

        if self.env.context.get('trigger') == 'qty':
            res = {'value': {'price_unit': res['value']['price_unit']}}

        if type not in ['out_invoice', 'out_refund']:
            return res
        if not partner_id or not product:
            return res

        if currency_id:
            currency = self.env['res.currency'].browse(currency_id)
            rounded_price_unit = currency.round(res['value']['price_unit'])
            if 'price_unit' not in res['value']\
                    or not res['value']['price_unit']\
                    or 'uos_id' in res['value']\
                    or 'quantity' in res['value']\
                    or rounded_price_unit == price_unit:
                product_data = self.env['product.product'].browse(product)
                price_unit = product_data.lst_price

                partner = self.env['res.partner'].browse(partner_id)
                pricelist = self._context.get('pricelist_id', False) or \
                    (partner.property_product_pricelist and
                     partner.property_product_pricelist.id) \
                    or None
                if pricelist:
                    pricelist = self.env['product.pricelist'].browse(pricelist)
                    if 'uos_id' in res['value'] and res['value']['uos_id'] and res['value']['uos_id'] != product_data.uom_id.id:
                        pricedict = pricelist.with_context(uom=res['value']['uos_id']).price_get(product, qty, partner_id)
                    else:
                        pricedict = pricelist.price_get(product, qty, partner_id)
                    price_unit = pricedict[pricelist.id]

                price_unit = pricelist.currency_id.compute(
                    price_unit, currency, round=True)

                price_unit = currency.round(price_unit)
                res['value']['price_unit'] = price_unit

        return res
