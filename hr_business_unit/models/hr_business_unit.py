# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class hr_business_unit(models.Model):
    _name = "hr.business.unit"
    _description = "Business Unit"

    name = fields.Char("Name")
    note = fields.Text("Note")
