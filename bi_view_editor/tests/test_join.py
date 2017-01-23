# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestBiViewEditor(common.TransactionCase):

    def setUp(self):
        super(TestBiViewEditor, self).setUp()
        self.partner_model_name = 'res.partner'
        self.partner_field_name = 'name'
        self.partner_company_field_name = 'company_id'
        self.company_model_name = 'res.company'
        self.company_field_name = 'name'

        self.bi_view1 = None

        Model = self.env['ir.model']
        ModelFields = self.env['ir.model.fields']

        self.partner_model = Model.search([
            ('model', '=', self.partner_model_name)
        ], limit=1)

        self.company_model = Model.search([
            ('model', '=', self.company_model_name)
        ], limit=1)

        self.partner_field = ModelFields.search([
            ('model', '=', self.partner_model_name),
            ('name', '=', self.partner_field_name)
        ], limit=1)

        self.partner_company_field = ModelFields.search([
            ('model', '=', self.partner_model_name),
            ('name', '=', self.partner_company_field_name)
        ], limit=1)

        self.company_field = ModelFields.search([
            ('model', '=', self.company_model_name),
            ('name', '=', self.company_field_name)
        ], limit=1)

        data = [
            {'model_id': self.partner_model.id,
             'name': self.partner_field_name,
             'model_name': self.partner_model.name,
             'model': self.partner_model_name,
             'custom': 0,
             'type': self.partner_field.ttype,
             'id': self.partner_field.id,
             'description': self.partner_field.field_description,
             'table_alias': 't0',
             'row': 0,
             'column': 1,
             'measure': 0
             },
            {'model_id': self.partner_model.id,
             'name': self.partner_company_field_name,
             'table_alias': 't0',
             'custom': 0,
             'relation': self.company_model_name,
             'model': self.partner_model_name,
             'model_name': self.partner_model.name,
             'type': self.partner_company_field.ttype,
             'id': self.partner_company_field.id,
             'join_node': 't1',
             'description': self.partner_company_field.field_description,
             'row': 0,
             'column': 0,
             'measure': 0
             },
            {'model_id': self.company_model.id,
             'name': 'name_1',
             'model_name': self.company_model.name,
             'model': self.company_model_name,
             'custom': 0,
             'type': self.company_field.ttype,
             'id': self.company_field.id,
             'description': self.company_field.field_description,
             'table_alias': 't1',
             'row': 1,
             'column': 0,
             'measure': 0
             }
        ]
        format_data = self.env['bve.view']._get_format_data(str(data))

        self.bi_view1_vals = {
            'state': 'draft',
            'data': format_data
        }

    def test_01_setup(self):
        self.assertIsNotNone(self.partner_model)
        self.assertIsNotNone(self.company_model)
        self.assertIsNotNone(self.partner_field)
        self.assertIsNotNone(self.partner_company_field)
        self.assertIsNotNone(self.company_field)

    def test_02_get_fields(self):
        Model = self.env['ir.model']
        fields = Model.get_fields(self.partner_model.id)
        self.assertIsInstance(fields, list)
        self.assertGreater(len(fields), 0)

    def test_03_get_join_nodes(self):
        new_field = {
            'model_id': self.partner_model.id,
            'name': self.partner_field_name,
            'custom': False,
            'id': self.partner_field.id,
            'model': self.partner_model_name,
            'type': self.partner_field.ttype,
            'model_name': self.partner_model.name,
            'description': self.partner_field.field_description
        }
        Model = self.env['ir.model']
        nodes = Model.get_join_nodes([], new_field)
        self.assertIsInstance(nodes, list)
        self.assertEqual(len(nodes), 0)

    def test_04_get_related_models(self):
        Model = self.env['ir.model']
        related_models = Model.get_related_models({
            't0': self.partner_model.id,
            't1': self.company_model.id
        })
        self.assertIsInstance(related_models, list)
        self.assertGreater(len(related_models), 0)

    def test_05_create_view(self):
        vals = self.bi_view1_vals
        vals.update({'name': 'Test View1'})
        bi_view1 = self.env['bve.view'].create(vals)
        self.assertIsNotNone(bi_view1)
        self.assertEqual(bi_view1.state, 'draft')
