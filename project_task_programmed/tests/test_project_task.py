# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase


class TestProjectTaskCreateAlerts(TransactionCase):

    def setUp(self):
        # Prepare some data for current test case

        def create_partner(Partner, name, delta):
            self.partner2 = Partner.create({
                'name': name,
                'date': str(date.today() + relativedelta(days=delta)),
            })

        super(TestProjectTaskCreateAlerts, self).setUp()

        self.project = self.env['project.project'].create({
            'name': 'Project Test'
        })

        Partner = self.env['res.partner']
        self.partner1 = create_partner(Partner, 'Partner 1', delta=1)
        self.partner2 = create_partner(Partner, 'Partner 2', delta=8)

        date_field = self.env.ref('base.field_res_partner_date')

        self.task_alert1 = self.env['project.task.alert'].create({
            'name': 'Task Alert Test1',
            'project_id': self.project.id,
            'days_delta': 3,
            'task_description': 'Description of Task Alert1',
            'date_field_id': date_field.id,
        })
        self.task_alert2 = self.env['project.task.alert'].create({
            'name': 'Task Alert Test2',
            'project_id': self.project.id,
            'days_delta': 8,
            'task_description': 'Description of Task Alert2',
            'date_field_id': date_field.id,
        })

    def test_create_alerts(self):
        self.task_alert1.create_task_alerts()
        task = self.env['project.task'].search([
            ('name', '=', 'Task Alert Test1')])
        self.assertEqual(len(task), 1)

    def test_run_alerts(self):
        self.env['project.task.alert'].run_task_alerts()
        task = self.env['project.task'].search([
            ('name', '=', 'Task Alert Test2')])
        self.assertEqual(len(task), 1)
