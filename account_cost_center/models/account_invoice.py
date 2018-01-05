# -*- coding: utf-8 -*-
# Copyright 2015-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    cost_center_id = fields.Many2one(
        'account.cost.center',
        string='Cost Center',
        help='Default Cost Center'
    )

    @api.model
    def line_get_convert(self, line, part):
        res = super(AccountInvoice, self).line_get_convert(line, part)
        if line.get('cost_center_id'):
            res['cost_center_id'] = line['cost_center_id']
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(AccountInvoice, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        if not self._context.get('cost_center_default', False):
            if view_type == 'form':
                view_obj = etree.XML(res['arch'])
                invoice_line = view_obj.xpath(
                    "//field[@name='invoice_line_ids']"
                )
                extra_ctx = "'cost_center_default': 1, " \
                    "'cost_center_id': cost_center_id"
                for el in invoice_line:
                    ctx = "{" + extra_ctx + "}"
                    if el.get('context'):
                        ctx = el.get('context')
                        ctx_strip = ctx.rstrip("}").strip().rstrip(",")
                        ctx = ctx_strip + ", " + extra_ctx + "}"

                    el.set('context', str(ctx))
                    res['arch'] = etree.tostring(view_obj)
        return res

    @api.model
    def invoice_line_move_line_get(self):
        res = super(AccountInvoice, self).invoice_line_move_line_get()

        for dict_data in res:
            invl_id = dict_data.get('invl_id')
            line = self.env['account.invoice.line'].browse(invl_id)
            if line.cost_center_id:
                dict_data['cost_center_id'] = line.cost_center_id.id

        return res
