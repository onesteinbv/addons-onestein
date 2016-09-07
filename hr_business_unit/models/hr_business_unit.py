# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class hr_business_unit(models.Model):
    _name = "hr.business.unit"
    _description = "Business Unit"

    name = fields.Char("Name")
    note = fields.Text("Note")
