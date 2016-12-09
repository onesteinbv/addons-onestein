# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MailFollowers(models.Model):
    _inherit = 'mail.followers'

    @api.model
    def create(self, vals):
        if not self._context.get('propagated', False):
            res_id = vals.get('res_id')
            partner_id = vals.get('partner_id')
            res_model = vals.get('res_model')
            is_model_project = res_model == 'project.project'
            is_model_analytic = res_model == 'account.analytic.account'
            new_vals = vals.copy()
            if is_model_project and res_id and partner_id:
                Project = self.env['project.project']
                project = Project.browse(res_id)
                if project.analytic_account_id:
                    found = self.search([
                        ('res_model', '=', 'account.analytic.account'),
                        ('res_id', '=', project.analytic_account_id.id),
                        ('partner_id', '=', partner_id)
                    ], limit=1)

                    if not found:
                        new_vals.update({
                            'res_model': 'account.analytic.account',
                            'res_id': project.analytic_account_id.id,
                            'partner_id': partner_id,
                        })
                        self.with_context(propagated=True).create(new_vals)

            elif is_model_analytic and res_id and partner_id:
                AnalyticAccount = self.env['account.analytic.account']
                analytic = AnalyticAccount.browse(res_id)
                projects = analytic.project_ids

                for project in projects:
                    found = self.search([
                        ('res_model', '=', 'project.project'),
                        ('res_id', '=', project.id),
                        ('partner_id', '=', partner_id)
                    ], limit=1)

                    if not found:
                        new_vals.update({
                            'res_model': 'project.project',
                            'res_id': project.id,
                            'partner_id': partner_id,
                        })
                        self.with_context(propagated=True).create(new_vals)

        return super(MailFollowers, self).create(vals)

    @api.multi
    def unlink(self):
        if not self._context.get('propagated', False):
            for follower in self:
                if follower.res_model == 'project.project':
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

                        if not found:
                            self.search([
                                ('res_model', '=', 'account.analytic.account'),
                                ('partner_id', '=', follower.partner_id.id),
                                ('res_id', '=', analytic.id)
                            ]).with_context(propagated=True).unlink()

                elif follower.res_model == 'account.analytic.account':
                    AnalyticAccount = self.env['account.analytic.account']
                    analytic = AnalyticAccount.browse(follower.res_id)
                    self.search([
                        ('res_model', '=', 'project.project'),
                        ('partner_id', '=', follower.partner_id.id),
                        ('res_id', 'in', analytic.project_ids.ids)
                    ]).with_context(propagated=True).unlink()

        return super(MailFollowers, self).unlink()

    @api.model
    def _align_analytic_to_project(self):
        self.env.cr.execute('''
            SELECT
                foll.id AS follower_id, foll.channel_id AS channel_id,
                foll.partner_id AS partner_id, proj.id AS project_id,
                acc.id AS account_id
            FROM
                mail_followers AS foll,
                project_project AS proj,
                account_analytic_account AS acc
            WHERE
                foll.res_model = 'project.project' AND
                foll.res_id = proj.id AND
                proj.analytic_account_id = acc.id AND
                NOT EXISTS(
                    SELECT *
                    FROM mail_followers AS foll2
                    WHERE
                        foll2.res_model = 'account.analytic.account' AND
                        foll2.partner_id = foll.partner_id AND
                        foll2.res_id = acc.id
                )
        ''')
        for record in self.env.cr.fetchall():
            self.create({
                'res_model': 'account.analytic.account',
                'res_id': record[4],
                'channel_id': record[1],
                'partner_id': record[2],
            })

    @api.model
    def _align_project_to_analytic(self):
        self.env.cr.execute('''
            SELECT
                foll.id AS follower_id, foll.channel_id AS channel_id,
                foll.partner_id AS partner_id, acc.id AS account_id,
                proj.id AS project_id
            FROM
                mail_followers AS foll,
                project_project AS proj,
                account_analytic_account AS acc
            WHERE
                foll.res_model = 'account.analytic.account' AND
                foll.res_id = acc.id AND
                proj.analytic_account_id = acc.id AND
                NOT EXISTS(
                    SELECT *
                    FROM mail_followers AS foll2
                    WHERE
                        foll2.res_model = 'project.project' AND
                        foll2.partner_id = foll.partner_id AND
                        foll2.res_id = proj.id
                )
        ''')
        for record in self.env.cr.fetchall():
            self.create({
                'res_model': 'project.project',
                'res_id': record[4],
                'channel_id': record[1],
                'partner_id': record[2],
            })
