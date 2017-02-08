# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class hr_employee(models.Model):
    _inherit = "hr.employee"

    business_unit_id = fields.Many2one('hr.business.unit', string="Business Unit")
