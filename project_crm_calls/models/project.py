# -*- coding: utf-8 -*-
# Copyright 2015 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ProjectProject(models.Model):

    _inherit = 'project.project'

    @api.multi
    def _calls_count(self):
        for project in self:
            project.calls_count = len(project.call_ids)

    call_ids = fields.One2many(
        'crm.phonecall',
        'project_id',
        string='Calls'
    )
    calls_count = fields.Integer(
        compute='_calls_count',
        string='Calls'
    )
