# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    pricelist_id = fields.Many2one(
        'product.pricelist',
        'Pricelist',
        help="Pricelist for current invoice.")

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        partner = self.partner_id
        if self.type in ['out_invoice', 'out_refund']:
            if partner:
                self.pricelist_id = partner.property_product_pricelist
            else:
                self.pricelist_id = None
        return res
