# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api

class res_company(models.Model):
    _inherit = "res.company"

    notify_template_id = fields.Many2one(
        'mail.template', string="Notify Email Template")
    expire_template_id = fields.Many2one(
        'mail.template', string="Expired Email Template")
