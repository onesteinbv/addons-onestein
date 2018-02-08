# Copyright 2016-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    notify_template_id = fields.Many2one(
        'mail.template',
        string='Notify Email Template'
    )
    expire_template_id = fields.Many2one(
        'mail.template',
        string='Expired Email Template'
    )
