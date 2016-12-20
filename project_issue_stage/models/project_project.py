# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.model
    def _get_issue_type_common(self):
        return self.env['project.issue.stage'].search([('case_default','=',1)])

    issue_stage_ids = fields.Many2many(
        'project.issue.stage',
        'project_issue_stage_rel',
        'project_id',
        'issue_stage_id',
        string='Issue Stages',
        default=_get_issue_type_common
    )
