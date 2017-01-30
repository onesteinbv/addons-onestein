# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectIssue(models.Model):

    _inherit = 'project.issue'

    issue_type_id = fields.Many2one(
        'project.issue.type',
        'Issue Type'
    )
