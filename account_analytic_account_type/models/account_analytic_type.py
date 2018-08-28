# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAnalyticType(models.Model):
    _name = "account.analytic.type"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    is_view = fields.Boolean()
