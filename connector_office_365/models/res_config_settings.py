# Copyright 2019 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    office_365_client_id = fields.Char(string='Client ID')
    office_365_client_secret = fields.Char(string='Client Secret')
    office_365_tenant_id = fields.Char(string='Tenant ID', default='common',
        help='Place here Tenant ID (or Application ID), if multi-tenant application, use "common" instead')

    @api.model
    def get_values(self):
        res = super().get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update({
            'office_365_tenant_id': get_param('office_365.tenant_id'),
            'office_365_client_id': get_param('office_365.client_id'),
            'office_365_client_secret': get_param('office_365.client_secret'),
        })
        return res

    @api.multi
    def set_values(self):
        super().set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('office_365.tenant_id', self.office_365_tenant_id)
        set_param('office_365.client_id', self.office_365_client_id)
        set_param('office_365.client_secret', self.office_365_client_secret)
