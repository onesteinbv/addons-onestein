# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _default_partner_country(self):
        return self.env.ref('base.nl')

    @api.model
    def default_get(self, fields):
        res = super(ResPartner, self).default_get(fields)
        res['lang'] = 'nl_NL'
        return res

    country_id = fields.Many2one(default=_default_partner_country)
