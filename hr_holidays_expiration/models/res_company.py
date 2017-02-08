# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class res_company(models.Model):
    _inherit = "res.company"

    notify_template_id = fields.Many2one(
        'email.template', string="Notify Email Template")
    expire_template_id = fields.Many2one(
        'email.template', string="Expired Email Template")
