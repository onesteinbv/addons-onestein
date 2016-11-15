# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    cost_center_budget_id = fields.Many2one(
        'crossovered.budget',
        string="Cost Center Budget",
        domain=[
            ('cost_center_id','!=',False)
        ],
        readonly=True)

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + \
            ", sub.cost_center_budget_id as cost_center_budget_id"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + \
            ", ail.cost_center_budget_id as cost_center_budget_id"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + \
            ", ail.cost_center_budget_id"
