# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_nl_tax_invoice_basis = fields.Boolean(
        string='NL Tax Invoice Basis',
        related='company_id.l10n_nl_tax_invoice_basis',
    )
