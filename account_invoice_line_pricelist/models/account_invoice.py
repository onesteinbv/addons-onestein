# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    pricelist_id = fields.Many2one(
        'product.pricelist',
        'Pricelist',
        help="Pricelist for current invoice.")

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
                            payment_term=False, partner_bank_id=False,
                            company_id=False):

        res = super(AccountInvoice, self).onchange_partner_id(
            type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False,
            company_id=False)

        if type in ['out_invoice', 'out_refund']:
            res['value'].update({
                'pricelist_id': None,
            })
            if partner_id:
                partner = self.env['res.partner'].browse(partner_id)
                if partner.property_product_pricelist:
                    res['value'].update({
                        'pricelist_id': partner.property_product_pricelist.id,
                    })
        return res
