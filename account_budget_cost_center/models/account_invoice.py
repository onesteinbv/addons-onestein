# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from lxml import etree


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    cost_center_budget_id = fields.Many2one(
        comodel_name='crossovered.budget',
        domain=[
            ('cost_center_id','!=',False)
        ],
        string='Cost Center Budget'
    )

    @api.model
    def line_get_convert(self, line, part, date):
        res = super(AccountInvoice, self).line_get_convert(line, part, date)
        if line.get('cost_center_budget_id'):
            res['cost_center_budget_id'] = line['cost_center_budget_id']
        return res

    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        res = super(AccountInvoice, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type,
            context=context, toolbar=toolbar, submenu=submenu)
        if not context:
            context = {}
        if not context.get('cost_center_budget_default', False):
            if view_type == 'form':
                view_obj = etree.XML(res['arch'])
                invoice_line = view_obj.xpath("//field[@name='invoice_line']")
                extra_ctx = "'cost_center_budget_default': 1, " \
                    "'cost_center_budget_id': cost_center_budget_id"
                for el in invoice_line:
                    ctx = el.get('context')
                    if ctx:
                        ctx_strip = ctx.rstrip("}").strip().rstrip(",")
                        ctx = ctx_strip + ", " + extra_ctx + "}"
                    else:
                        ctx = "{" + extra_ctx + "}"
                    el.set('context', str(ctx))
                    res['arch'] = etree.tostring(view_obj)
        return res
