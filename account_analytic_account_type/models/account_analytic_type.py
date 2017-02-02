# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticType(models.Model):
    _name = "account.analytic.type"

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    is_view = fields.Boolean('Is View')
