# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestProjectIssueStage(common.TransactionCase):

    def setUp(self):
        super(TestProjectIssueStage, self).setUp()
        self.Stage = self.env['project.issue.stage']
        self.Issue = self.env['project.issue']
        self.Project = self.env['project.project']

        self.project = self.Project.create({
            'name': 'Project Test'
        })

        self.stage_1 = self.Stage.create({
            'name': 'Stage 1',
            'fold': False,
        })

        self.stage_2 = self.Stage.create({
            'name': 'Stage 2',
            'fold': True,
        })

        self.stage_3 = self.Stage.create({
            'name': 'Stage 3',
            'fold': False,
            'sequence': 5,
        })

        self.issue_1 = self.Issue.with_context(
            default_project_id=self.project.id
        ).create({
            'name': 'Journal 1',
            'kanban_state': 'normal',
            'issue_stage_id': self.stage_1.id,
        })

        self.issue_2 = self.Issue.with_context(
            default_project_id=self.project.id
        ).create({
            'name': 'Journal 1',
            'issue_stage_id': self.stage_1.id,
        })

        self.issue_3 = self.Issue.with_context(
            default_project_id=self.project.id
        ).create({
            'name': 'Journal 1',
        })

    def test_01_issue_write(self):
        self.issue_1.write({'issue_stage_id': self.stage_3.id})
        self.issue_2.write({'issue_stage_id': self.stage_2.id})
