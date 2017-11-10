# -*- coding: utf-8 -*-
# Copyright 2016-2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
try:
    from stdnum.nl import bsn
except ImportError:
    _logger.debug('Cannot `import stdnum.nl.bsn`.')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bsn_number = fields.Char(
        string='BSN',
        groups='hr.group_hr_user'
    )

    @api.multi
    @api.onchange('bsn_number')
    def onchange_bsn_number(self):
        warning = {}
        for partner in self:
            if partner.bsn_number:
                # properly format the entered BSN
                partner.bsn_number = bsn.format(partner.bsn_number)

                # check is valid, otherwise display a warning
                warning = partner._warn_bsn_invalid()

                # search for another partner with the same BSN
                args = [('bsn_number', '=', partner.bsn_number),
                        ('name', '!=', partner.name)]

                # refine search in case of multicompany setting
                if partner.company_id:
                    args += [('company_id', '=', partner.company_id.id)]
                other_partner = self.search(args, limit=1)

                # if another partner exists, display a warning
                if other_partner:
                    warning = other_partner._warn_bsn_existing()
        return {'warning': warning, }

    @api.multi
    def _warn_bsn_invalid(self):
        self.ensure_one()
        warning = {}
        if not bsn.is_valid(self.bsn_number):
            msg = _('The BSN you entered (%s) is not valid.')
            warning = {
                'title': _('Warning!'),
                'message': msg % self.bsn_number,
            }
        return warning

    def _warn_bsn_existing(self):
        self.ensure_one()
        msg = _('Another person (%s) has the same BSN (%s).')
        warning = {
            'title': _('Warning!'),
            'message': msg % (self.name, self.bsn_number)
        }
        return warning
