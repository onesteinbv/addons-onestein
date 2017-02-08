# -*- coding: utf-8 -*-
# Copyright 2015 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class project_task(models.Model):
    _inherit = 'project.task'

    alert_model_name = fields.Char('Alert Model Name')
    alert_res_id = fields.Integer('Alert Resource ID')
    alert_field_name = fields.Char('Alert Date Field Name')
