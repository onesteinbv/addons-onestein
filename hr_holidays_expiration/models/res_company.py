# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class res_company(models.Model):
    _inherit = "res.company"

    notify_template_id = fields.Many2one(
        'email.template', string="Notify Email Template")
    expire_template_id = fields.Many2one(
        'email.template', string="Expired Email Template")
