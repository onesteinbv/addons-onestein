# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class HrHolidaysPublic(models.Model):
    _inherit = 'hr.holidays.public'

    state = fields.Selection(
        [('draft', 'To Approve'),
         ('validate', 'Approved')],
        'Status', readonly=True,
        track_visibility='onchange', copy=False,
        help="""The status is set to 'To Submit',
              when a holiday request is created.
              \nThe status is 'Approved', when holiday request
              is approved by manager.""",
        default='draft')
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.user.company_id,
        string='Company')

    @api.multi
    def _reinit(self):
        for public_holiday in self:
            _logger.debug(
                "hr_public_holiday reinit: %s" %
                (public_holiday.display_name,)
            )
            public_holiday.line_ids.with_context(
                company_id=public_holiday.company_id
            ).reinit()

    @api.multi
    def _reset(self):
        for public_holiday in self:
            _logger.debug(
                "hr_public_holiday reset: %s" %
                (public_holiday.display_name,)
            )
            public_holiday.line_ids.reset()

    def validate(self):
        self._reinit()
        self.state = 'validate'

    def reset(self):
        self._reset()
        self.state = 'draft'
