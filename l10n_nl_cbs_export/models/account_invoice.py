# -*- coding: utf-8 -*-
# Copyright 2017 Odoo Experts (<https://www.odooexperts.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    cbs_export_id = fields.Many2one('cbs.export.file', 'CBS Export')
