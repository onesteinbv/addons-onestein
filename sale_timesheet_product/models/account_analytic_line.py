# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def _get_timesheet_cost(self, values):
        res = super(AccountAnalyticLine, self)._get_timesheet_cost(values)

        if not values.get('project_id') and not self.project_id:
            return res

        product = self._get_sale_order_line_employee_product(values)
        if product:
            cost = product and product.list_price or 0.0
            uom = product.uom_id
            unit_amount = values.get('unit_amount', 0.0) or self.unit_amount
            # Nominal employee cost = 1 * company project UoM
            # (project_time_mode_id)
            res.update({
                'amount': -unit_amount * cost,
                'product_uom_id': uom.id,
            })
        return res

    def _get_sale_order_line(self, vals=None):
        result = dict(vals or {})
        if not self.project_id or not vals.get('user_id'):
            return super(AccountAnalyticLine, self)._get_sale_order_line(
                vals=result
            )

        product = self._get_sale_order_line_employee_product(vals)
        if not product or result.get('so_line') or self.so_line:
            return super(AccountAnalyticLine, self)._get_sale_order_line(
                vals=result
            )

        sol = self.env['sale.order.line'].search([
            ('order_id.project_id', '=', self.account_id.id),
            ('state', '=', 'sale'),
            ('product_id.id', '=', product.id)],
            limit=1)
        if not sol:
            sol = self._create_sale_order_line_employee_product(product)
        if sol:
            result.update({
                'so_line': sol.id,
                'product_id': sol.product_id.id,
            })
            result.update(self._get_timesheet_cost(result))

        return super(AccountAnalyticLine, self)._get_sale_order_line(
            vals=result
        )

    def _get_sale_order_line_user_id(self, vals):
        user_id = vals.get('user_id') or self.user_id.id
        return user_id or self._default_user()

    def _get_sale_order_line_employee_product(self, vals):
        user_id = self._get_sale_order_line_user_id(vals)
        emp = self.env['hr.employee'].search([
            ('user_id', '=', user_id)
        ], limit=1)
        return emp and emp.product_id or False

    def _create_sale_order_line_employee_product(self, product):
        sol = False
        order = self.env['sale.order'].search([
            ('project_id', '=', self.account_id.id),
            ('state', '=', 'sale')
        ], limit=1)
        if order:
            order_line_vals = self._get_sale_order_line_vals(
                order,
                product.list_price or 0.0
            )
            if order_line_vals:
                order_line_vals.update({'product_id': product.id})
                sol = self.env['sale.order.line'].create(order_line_vals)
                sol._compute_tax_id()
        return sol
