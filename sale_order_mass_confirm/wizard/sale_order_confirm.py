# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderConfirmWizard(models.TransientModel):
    _name = "sale.order.confirm.wizard"
    _description = "Wizard - Sale Order Confirm"

    @api.multi
    def confirm_sale_orders(self):
        self.ensure_one()
        active_ids = self.env.context.get('active_ids')
        orders = self.env['sale.order'].browse(active_ids)
        orders = orders.filtered(lambda o: o.state in ['draft', 'sent'])
        orders.action_confirm()
