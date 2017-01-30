# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MailFollowers(models.Model):
    _inherit = 'mail.followers'

    @api.model
    def _create_if_missing(self, res_model, res_id, partner_id, new_vals):
        found = self.search([
            ('res_model', '=', res_model),
            ('res_id', '=', res_id),
            ('partner_id', '=', partner_id)
        ], limit=1)

        if not found:
            new_vals.update({
                'res_model': res_model,
                'res_id': res_id,
                'partner_id': partner_id,
            })
            self.with_context(propagated=True).create(new_vals)

    @api.model
    def _create_mirror(self, res_id, partner_id, new_vals, res_model):
        Model = self.env[res_model]
        obj = Model.browse(res_id)
        if res_model == 'project.project':
            opposing_model = 'account.analytic.account'
            if obj.analytic_account_id:
                self._create_if_missing(
                    opposing_model,
                    obj.analytic_account_id.id,
                    partner_id,
                    new_vals)

        elif res_model == 'account.analytic.account':
            opposing_model = 'project.project'
            projects = obj.project_ids

            for project in projects:
                self._create_if_missing(
                    opposing_model,
                    project.id,
                    partner_id,
                    new_vals)

    @api.model
    def create(self, vals):
        if not self._context.get('propagated', False):
            res_id = vals.get('res_id')
            partner_id = vals.get('partner_id')
            res_model = vals.get('res_model')
            new_vals = vals.copy()
            if res_id and partner_id:
                self._create_mirror(res_id, partner_id, new_vals, res_model)
        return super(MailFollowers, self).create(vals)

    @api.model
    def _unlink_mirror(self, res_model, follower):

        partner_id = follower.partner_id.id
        if res_model == 'project.project':
            Project = self.env['project.project']
            project = Project.browse(follower.res_id)
            analytic = project.analytic_account_id

            if analytic.project_ids:
                found = self.search([
                    ('res_model', '=', 'project.project'),
                    ('partner_id', '=', follower.partner_id.id),
                    ('res_id', '!=', follower.res_id),
                    ('res_id', 'in', analytic.project_ids.ids)
                ], limit=1)
                self._unlink_if_missing(
                    found,
                    'account.analytic.account',
                    partner_id,
                    [analytic.id]
                )

        elif follower.res_model == 'account.analytic.account':
            AnalyticAccount = self.env['account.analytic.account']
            analytic = AnalyticAccount.browse(follower.res_id)
            self._unlink_if_missing(
                False,
                'project.project',
                partner_id,
                analytic.project_ids.ids
            )

    @api.model
    def _unlink_if_missing(self, found, res_model, partner_id, res_id):
        if not found:
            self.search([
                ('res_model', '=', res_model),
                ('partner_id', '=', partner_id),
                ('res_id', 'in', res_id)
            ]).with_context(propagated=True).unlink()

    @api.multi
    def unlink(self):
        if not self._context.get('propagated', False):
            for follower in self:
                res_model = follower.res_model
                self._unlink_mirror(res_model, follower)

        return super(MailFollowers, self).unlink()

    @api.model
    def _align_followers(self, target, origin):
        s1 = ''
        w1 = ''
        w2 = ''

        if target == 'account.analytic.account':
            s1 = 'acc.id AS account_id'
            w1 = 'proj.id'
            w2 = 'acc.id'

        elif target == 'project.project':
            s1 = 'proj.id AS project_id'
            w1 = 'acc.id'
            w2 = 'proj.id'

        self.env.cr.execute('''
            SELECT
                foll.id AS follower_id, foll.channel_id AS channel_id,
                foll.partner_id AS partner_id, proj.id AS project_id,
            ''' + s1 + '''
            FROM
                mail_followers AS foll,
                project_project AS proj,
                account_analytic_account AS acc
            WHERE
                foll.res_model = %s AND
                foll.res_id = '''+w1+''' AND
                proj.analytic_account_id = acc.id AND
                foll.partner_id IS NOT NULL AND
                NOT EXISTS(
                    SELECT *
                    FROM mail_followers AS foll2
                    WHERE
                        foll2.res_model = %s AND
                        foll2.partner_id = foll.partner_id AND
                        foll2.res_id = '''+w2+'''
                )
        ''', (origin, target,))

        for record in self.env.cr.fetchall():
            self.create({
                'res_model': target,
                'res_id': record[4],
                'channel_id': record[1],
                'partner_id': record[2],
            })
