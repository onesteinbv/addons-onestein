# -*- coding: utf-8 -*-
# Copyright 2015-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models

NO_BI_MODELS = [
    'temp.range',
    'account.statement.operation.template',
    'fetchmail.server'
]

NO_BI_FIELDS = [
    'id',
    'create_uid',
    'create_date',
    'write_uid',
    'write_date'
]

NO_BI_TTYPES = [
    'many2many',
    'one2many',
    'html',
    'binary',
    'reference'
]


def dict_for_field(field):
    return {
        'id': field.id,
        'name': field.name,
        'description': field.field_description,
        'type': field.ttype,
        'relation': field.relation,
        'custom': False,
        'model_id': field.model_id.id,
        'model': field.model_id.model,
        'model_name': field.model_id.name
    }


def dict_for_model(model):
    return {
        'id': model.id,
        'name': model.name,
        'model': model.model
    }


class IrModel(models.Model):
    _inherit = 'ir.model'

    @api.model
    def _filter_bi_fields(self, ir_model_field_obj):
        name = ir_model_field_obj.name
        model = ir_model_field_obj.model_id
        model_name = model.model
        Model = self.env[model_name]
        if name in Model._fields:
            f = Model._fields[name]
            return f.store
        return False

    @api.model
    def _filter_bi_models(self, model):
        check_model_name = self._filter_bi_models_check_model_name(model)
        if not check_model_name:
            return False
        if model['name'] == 'Unknow' or '.' in model['name']:
            return False
        return self.env['ir.model.access'].check(
            model['model'], 'read', False)

    @api.model
    def _filter_bi_models_check_model_name(self, model):
        model_name = model['model']
        if model_name in NO_BI_MODELS:
            return False
        if model_name.startswith('workflow') or \
                model_name.startswith('ir.') or \
                model_name.startswith('base_'):
            return False
        if 'mail' in model_name or \
                '_' in model_name or \
                'report' in model_name or \
                'edi.' in model_name:
            return False
        return True

    @api.model
    def get_related_fields(self, model_ids):
        """ Return list of field dicts for all fields that can be
            joined with models in model_ids
        """
        Model = self.env['ir.model']
        domain = [('id', 'in', model_ids.values())]
        models = Model.sudo().search(domain)
        model_names = {}
        for model in models:
            model_names.update({model.id: model.model})

        related_fields = self._get_related_fields_list(model_ids, model_names)
        return related_fields

    @api.model
    def _get_related_fields_list(self, model_ids, model_names):

        Fields = self.env['ir.model.fields']
        lfields = self._get_left_fields(Fields, model_ids, model_names)
        rfields = self._get_right_fields(Fields, model_ids, model_names)

        relation_list = []
        model_list = []
        for model in model_ids.items():
            for field in lfields:
                if model_names[model[1]] == field['relation']:
                    relation_list.append(
                        dict(field, join_node=model[0])
                    )
            for field in rfields:
                if model[1] == field['model_id']:
                    model_list.append(
                        dict(field, table_alias=model[0])
                    )
        related_fields = relation_list + model_list
        return related_fields

    @api.model
    def _get_right_fields(self, Fields, model_ids, model_names):
        rfields = []
        domain = [('model_id', 'in', model_ids.values()),
                  ('ttype', 'in', ['many2one'])]
        for field in filter(
                self._filter_bi_fields,
                Fields.sudo().search(domain)):
            for model in model_ids.items():
                if model[1] == field.model_id.id:
                    rfields.append(
                        dict(dict_for_field(field),
                             join_node=-1,
                             table_alias=model[0])
                    )
        return rfields

    @api.model
    def _get_left_fields(self, Fields, model_ids, model_names):
        lfields = []
        domain = [('relation', 'in', model_names.values()),
                  ('ttype', 'in', ['many2one'])]
        for field in filter(
                self._filter_bi_fields,
                Fields.sudo().search(domain)):
            for model in model_ids.items():
                if model_names[model[1]] == field['relation']:
                    lfields.append(
                        dict(dict_for_field(field),
                             join_node=model[0],
                             table_alias=-1)
                    )
        return lfields

    @api.model
    def get_related_models(self, model_ids):
        """ Return list of model dicts for all models that can be
            joined with models in model_ids
        """
        related_fields = self.get_related_fields(model_ids)
        return sorted(filter(
            self._filter_bi_models,
            [{'id': model.id, 'name': model.name, 'model': model.model}
             for model in self.env['ir.model'].sudo().search(
                ['|',
                 ('id', 'in', model_ids.values() + [
                     f['model_id']
                     for f in related_fields if f['table_alias'] == -1]),
                 ('model', 'in', [
                     f['relation']
                     for f in related_fields if f['join_node'] == -1])])]),
            key=lambda x: x['name'])

    @api.model
    def get_models(self):
        """ Return list of model dicts for all available models.
        """
        models_domain = [('transient', '=', False)]
        return sorted(filter(
            self._filter_bi_models,
            [dict_for_model(model)
                for model in self.search(models_domain)]),
            key=lambda x: x['name'])

    @api.model
    def get_join_nodes(self, field_data, new_field):
        """ Return list of field dicts of join nodes

            Return all possible join nodes to add new_field to the query
            containing model_ids.
        """
        model_ids = self._get_model_ids(field_data)
        keys = [(field['table_alias'], field['id'])
                for field in field_data if field.get('join_node', -1) != -1]
        join_nodes = self._get_join_nodes_dict(model_ids, new_field)
        return filter(
            lambda x: 'id' not in x or
                      (x['table_alias'], x['id']) not in keys, join_nodes)

    @api.model
    def _get_join_nodes_dict(self, model_ids, new_field):
        join_nodes = []
        for alias, model_id in model_ids.items():
            if model_id == new_field['model_id']:
                join_nodes.append({'table_alias': alias})
        for d in self.get_related_fields(model_ids):
            if d['relation'] == new_field['model'] and \
                    d['join_node'] == -1 or \
                    d['model_id'] == new_field['model_id'] and \
                    d['table_alias'] == -1:
                join_nodes.append(d)
        return join_nodes

    @api.model
    def _get_model_ids(self, field_data):
        model_ids = dict([(field['table_alias'],
                           field['model_id']) for field in field_data])
        return model_ids

    @api.model
    def get_fields(self, model_id):
        bi_field_domain = [
            ('model_id', '=', model_id),
            ('name', 'not in', NO_BI_FIELDS),
            ('ttype', 'not in', NO_BI_TTYPES)
        ]
        Fields = self.env['ir.model.fields']
        fields = filter(
            self._filter_bi_fields,
            Fields.sudo().search(bi_field_domain)
        )
        fields_dict = []
        for field in fields:
            fields_dict.append(
                {'id': field.id,
                 'model_id': model_id,
                 'name': field.name,
                 'description': field.field_description,
                 'type': field.ttype,
                 'custom': False,
                 'model': field.model_id.model,
                 'model_name': field.model_id.name
                 }
            )
        sorted_fields = sorted(
            fields_dict,
            key=lambda x: x['description'],
            reverse=True
        )
        return sorted_fields

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        if self._context and self._context.get('bve'):
            vals['state'] = 'base'
        res = super(IrModel, self).create(vals)

        # this sql update is necessary since a write method here would
        # be not working (an orm constraint is restricting the modification
        # of the state field while updating ir.model)
        q = ("""UPDATE ir_model SET state = 'manual'
               WHERE id = """ + str(res.id))

        self.env.cr.execute(q)

        return res
