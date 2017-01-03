# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import tools
from openerp import fields, models
import openerp.addons.decimal_precision as dp


class AccountEntriesReport(models.Model):
    _inherit = "account.entries.report"

    cost_center_id = fields.Many2one('account.cost.center', 'Cost Center')

    def _select(self):
        select_str = super(AccountEntriesReport, self)._select()
        select_str += """
            ,l.cost_center_id as cost_center_id
        """
        return select_str