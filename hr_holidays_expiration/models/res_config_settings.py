# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    notify_template_id = fields.Many2one(
        'mail.template',
        related='company_id.notify_template_id'
    )
    expire_template_id = fields.Many2one(
        'mail.template',
        related='company_id.expire_template_id'
    )

    auto_approve_on_leave_type_archival = fields.Boolean(
        related='company_id.auto_approve_on_leave_type_archival'
    )
