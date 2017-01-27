# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ProjectIssue(models.Model):
    _inherit = "project.issue"

    issue_created = fields.Boolean(default=True)

    _track = {
        'issue_stage_id': {
            # this is only an heuristics; depending on your particular stage configuration it may not match all 'new' stages
            'project_issue.mt_issue_new': lambda self, cr, uid, obj,
                                                 ctx=None: obj.issue_stage_id and obj.issue_created,
            'project_issue_stage.mt_issue_stage': lambda self, cr, uid, obj,
                                                   ctx=None: obj.issue_stage_id and not obj.issue_created,
        },
        'stage_id': {

        },
        'user_id': {
            'project_issue.mt_issue_assigned': lambda self, cr, uid, obj, ctx=None: obj.user_id and obj.user_id.id,
        },
        'kanban_state': {
            'project_issue.mt_issue_blocked': lambda self, cr, uid, obj, ctx=None: obj.kanban_state == 'blocked',
            'project_issue.mt_issue_ready': lambda self, cr, uid, obj, ctx=None: obj.kanban_state == 'done',
        },
    }


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
        index=True,
        domain="[('project_ids', '=', project_id)]",
        copy=False,
        default=_get_default_issue_stage_id
    )

    @api.multi
    def _read_group_issue_stage_ids(
            self, domain, read_group_order=None, access_rights_uid=None):
        access_rights_uid = access_rights_uid or self.env.uid
        ProjectIssueStage = self.env['project.issue.stage']
        order = ProjectIssueStage._order
        # lame hack to allow reverting search,
        # should just work in the trivial case
        if read_group_order == 'stage_id desc':
            order = "%s desc" % order
        # retrieve project_id from the context,
        # add them to already fetched columns (ids)
        default_project_id = self.env.context.get('default_project_id', None)
        if default_project_id:
            search_domain = ['|',
                             ('project_ids', '=', default_project_id),
                             ('id', 'in', self.ids)]
        else:
            search_domain = [('id', 'in', self.ids)]
        # perform search
        project_issue_stages = ProjectIssueStage.sudo(access_rights_uid).search(
            search_domain,
            order=order
        )
        result = project_issue_stages.sudo(access_rights_uid).name_get()
        # restore order of the search
        project_issue_stage_ids = project_issue_stages.mapped('id')
        result.sort(
            lambda x, y: cmp(
                project_issue_stage_ids.index(x[0]),
                project_issue_stage_ids.index(y[0])
            )
        )
        fold = {
            project_issue_stage.id: project_issue_stage.fold
            for project_issue_stage in project_issue_stages}
        return result, fold

    _group_by_full = {
        'issue_stage_id': _read_group_issue_stage_ids
    }

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
            vals['issue_created'] = False
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
        if 'stage_id' in res:
            del res['stage_id']
        return res
