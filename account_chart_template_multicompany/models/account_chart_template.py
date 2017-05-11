# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    @api.multi
    def try_loading_for_current_company(self):
        self.ensure_one()
        res = super(AccountChartTemplate,
                    self).try_loading_for_current_company()
        company_list = self.env['res.company'].search([
            ('id', '!=', self.env.user.company_id.id)
        ])
        for company in company_list:
            # If we don't have any chart of account on this company,
            # install this chart of account
            if not company.chart_template_id:
                wizard = self.env['wizard.multi.charts.accounts'].create({
                    'company_id': company.id,
                    'chart_template_id': self.id,
                    'code_digits': self.code_digits,
                    'transfer_account_id': self.transfer_account_id.id,
                    'currency_id': self.currency_id.id,
                    'bank_account_code_prefix': self.bank_account_code_prefix,
                    'cash_account_code_prefix': self.cash_account_code_prefix,
                })
                wizard.onchange_chart_template_id()
                wizard.execute()
        return res
