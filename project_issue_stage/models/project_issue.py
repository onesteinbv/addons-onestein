# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectIssue(models.Model):
    _inherit = "project.issue"

    @api.model
    def _get_default_issue_stage_id(self):
        return self.issue_stage_find(
            self.env.context.get('default_project_id'),
            [('fold', '=', False)]
        )

    issue_stage_id = fields.Many2one(
        'project.issue.stage',
        string='Issue Stage',
        track_visibility='onchange',
        group_expand='_read_group_stage_ids',
        index=True,
        domain="[('project_ids', '=', project_id)]",
        copy=False,
        default=_get_default_issue_stage_id
    )

    @api.model
    def create(self, vals):
        if 'issue_stage_id' in vals:
            vals.update(self.update_date_closed_issue(vals['issue_stage_id']))
        return super(ProjectIssue, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'issue_stage_id' in vals:
            vals.update(self.update_date_closed_issue(vals['issue_stage_id']))
            vals['date_last_stage_update'] = fields.Datetime.now()
            if 'kanban_state' not in vals:
                vals['kanban_state'] = 'normal'
        return super(ProjectIssue, self).write(vals)

    def update_date_closed_issue(self, issue_stage_id):
        IssueStage = self.env['project.issue.stage']
        project_issue_stage = IssueStage.browse(issue_stage_id)
        if project_issue_stage.fold:
            return {'date_closed': fields.Datetime.now()}
        return {'date_closed': False}

    def issue_stage_find(self, project_id, domain=None, order='sequence'):
        search_domain = list(domain) if domain else []
        if project_id:
            search_domain += [('project_ids', '=', project_id)]
        project_issue_stage = self.env['project.issue.stage'].search(
            search_domain,
            order=order,
            limit=1
        )
        return project_issue_stage

    @api.multi
    def _track_template(self, tracking):
        self.ensure_one()
        res = super(ProjectIssue, self)._track_template(tracking)
        res.pop('stage_id', None)
        return res

    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'issue_stage_id' in init_values:
            if self.issue_stage_id:
                if self.issue_stage_id.sequence <= 1:  # start stage -> new
                    return 'project_issue.mt_issue_new'
        if 'issue_stage_id' in init_values:
            return 'project_issue.mt_issue_stage'
        return super(ProjectIssue, self)._track_subtype(init_values)
