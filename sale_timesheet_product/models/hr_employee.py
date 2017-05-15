# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    product_id = fields.Many2one(
        'product.product',
        'Product',
        help="If you want to reinvoice working time of employees, "
             "link this employee to a service to determinate "
             "the cost price of the job."
    )
