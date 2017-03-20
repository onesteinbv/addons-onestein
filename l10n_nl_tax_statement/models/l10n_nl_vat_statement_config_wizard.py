# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class VatStatementConfigWizard(models.TransientModel):
    _name = 'l10n.nl.vat.statement.config.wizard'
