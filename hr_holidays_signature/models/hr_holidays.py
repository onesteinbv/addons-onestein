# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    manager_signature = fields.Binary('Signature manager')
