# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    pricelist_id = fields.Many2one(
        'product.pricelist',
        'Pricelist',
        help="Pricelist for current invoice.")
    partner_pricelist_id = fields.Many2one(
        related='partner_id.property_product_pricelist',
        comodel_name='product.pricelist',
        readonly=True,
        string='Default Pricelist')
