# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields, api, _


class AccountAccountType(models.Model):
    _inherit = 'account.account.type'

    costcenter_policy = fields.Selection(
        '_get_policies', string='Policy for cost center dimension',
        required=True, default=lambda self: self._default_policy())

    # @api.model
    # def _get_costcenter_policies(self):
    #     return [('optional', _('Optional')),
    #             ('always', _('Always')),
    #             ('never', _('Never'))]
    #
    # @api.model
    # def _default_costcenter_policy(self):
    #     return 'optional'
