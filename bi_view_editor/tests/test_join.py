# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common


class TestBiViewEditor(common.TransactionCase):

    def test_01_create_view(self):

        partner_model_name = 'res.partner'
        partner_field_name = 'name'
        partner_company_id_field_name = 'company_id'
        company_model_name = 'res.company'
        company_field_name = 'name'

        partner_model = self.env['ir.model'].search([
            ('model', '=', partner_model_name)
        ], limit=1)
        self.assertIsNotNone(partner_model)

        company_model = self.env['ir.model'].search([
            ('model', '=', company_model_name)
        ], limit=1)
        self.assertIsNotNone(company_model)

        self.env['ir.model'].get_fields(partner_model.id)

        partner_field = self.env['ir.model.fields'].search([
            ('model', '=', partner_model_name),
            ('name', '=', partner_field_name)
        ], limit=1)
        self.assertIsNotNone(partner_field)

        partner_company_id_field = self.env['ir.model.fields'].search([
            ('model', '=', partner_model_name),
            ('name', '=', partner_company_id_field_name)
        ], limit=1)
        self.assertIsNotNone(partner_company_id_field)

        company_field = self.env['ir.model.fields'].search([
            ('model', '=', company_model_name),
            ('name', '=', company_field_name)
        ], limit=1)
        self.assertIsNotNone(company_field)

        new_field = {
            'model_id': partner_model.id,
            'name': partner_field_name,
            'custom': False,
            'id': partner_field.id,
            'model': partner_model_name,
            'type': partner_field.ttype,
            'model_name': partner_model.name,
            'description': partner_field.field_description
        }

        self.env['ir.model'].get_join_nodes([], new_field)

        self.env['ir.model'].get_related_models({
            't0': partner_model.id,
            't1': company_model.id
        })

        bi_view1 = self.env['bve.view'].create({
            'name': 'View Test1',
            'state': 'draft',
            'data': [
                {'model_id': partner_model.id,
                 'name': partner_field_name,
                 'model_name': partner_model.name,
                 'model': partner_model_name,
                 'custom': False,
                 'type': partner_field.ttype,
                 'id': partner_field.id,
                 'description': partner_field.field_description,
                 'table_alias': 't0',
                 'row': False,
                 'column': True,
                 'measure': False
                 },
                {'model_id': partner_model.id,
                 'name': partner_company_id_field_name,
                 'table_alias': 't0',
                 'custom': False,
                 'relation': company_model_name,
                 'model': partner_model_name,
                 'model_name': partner_model.name,
                 'type': partner_company_id_field.ttype,
                 'id': partner_company_id_field.id,
                 'join_node': 't1',
                 'description': partner_company_id_field.field_description,
                 'row': False,
                 'column': False,
                 'measure': False
                 },
                {'model_id': company_model.id,
                 'name': 'name_1',
                 'model_name': company_model.name,
                 'model': company_model_name,
                 'custom': False,
                 'type': company_field.ttype,
                 'id': company_field.id,
                 'description': company_field.field_description,
                 'table_alias': 't1',
                 'row': True,
                 'column': False,
                 'measure': False}]
                 }
        )
        self.assertIsNotNone(bi_view1)
