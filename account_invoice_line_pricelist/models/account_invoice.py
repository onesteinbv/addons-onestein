# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    pricelist_id = fields.Many2one(
        'product.pricelist',
        'Pricelist',
        help='Pricelist for current invoice.'
    )

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        if self.type in ['out_invoice', 'out_refund']:
            self.pricelist_id = None
            if self.partner_id:
                self.pricelist_id = self.partner_id.property_product_pricelist
        return res

    @api.multi
    def write(self, vals):
        """
        Update pricelist_id whenever missing, before real write()
        Remember: do *not* update rec.pricelist_id directly! that triggers write()
        """
        for rec in self:
            if ('type' in vals and vals['type'] in ['out_invoice', 'out_refund']) or (rec.type in ['out_invoice', 'out_refund']):
                if 'partner_id' in vals:
                    #INSERT/UPDATE partner
                    if not 'pricelist_id' in vals:
                        vals['pricelist_id'] = vals['partner_id'].property_product_pricelist
                else:
                    #UPDATE record
                    if ((not rec.pricelist_id) or(not rec.pricelist_id.id)) and (rec.partner_id) and (rec.partner_id.property_product_pricelist) and (rec.partner_id.property_product_pricelist.id):
                        vals['pricelist_id'] = rec.partner_id.property_product_pricelist.id
        return super(AccountInvoice, self).write(vals)
