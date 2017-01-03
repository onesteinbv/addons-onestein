# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import fields, models


class AccountMoveLine(models.Model):
    """
    This module adds fields to facilitate UI enforcement
    of analytic dimensions.
    """
    _inherit = 'account.move.line'

    costcenter_policy = fields.Selection(
        string='Policy for costcenter dimension',
        related='account_id.costcenter_policy', readonly=True)
