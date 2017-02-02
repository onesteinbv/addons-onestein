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
            return Partner.create({
                'name': name,
                'date': str(date.today() + relativedelta(days=delta)),
            })

        def create_task_alerts(parameter_list):
            date_field = self.env.ref('base.field_res_partner_date')
            Alert = self.env['project.task.alert']
            defaults = {
                'project_id': self.project.id,
                'date_field_id': date_field.id,
            }
            return (Alert.create(
                (defaults.copy()).update(args)) for args in parameter_list)

        super(TestProjectTaskCreateAlerts, self).setUp()

        self.project = self.env['project.project'].create({
            'name': 'Project Test'
        })

        Partner = self.env['res.partner']
        self.partner1 = create_partner(Partner, 'Partner 1', delta=1)
        self.partner2 = create_partner(Partner, 'Partner 2', delta=8)

        self.task_alert1, self.task_alert2 = create_task_alerts([
            {
                'name': 'Task Alert Test1',
                'days_delta': 3,
                'task_description': 'Description of Task Alert1',
            },
            {
                'name': 'Task Alert Test2',
                'days_delta': 8,
                'task_description': 'Description of Task Alert2',
            }
        ])

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
