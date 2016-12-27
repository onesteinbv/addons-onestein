# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
try:
    from stdnum.nl import postcode
except ImportError:
    _logger.debug('Cannot `import stdnum.nl.postcode`.')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.onchange('zip')
    def onchange_zip_l10n_nl_postcode(self):
        warning = {}
        if self.env.context.get('skip_postcode_check'):
            return {}
        for partner in self:
            if partner.zip:
                country = partner.country_id
                if not country or country != self.env.ref('base.nl'):
                    continue

                # check is valid, otherwise display a warning
                if not postcode.is_valid(partner.zip):
                    msg = _('The Postcode you entered (%s) is not valid.')
                    warning = {
                        'title': _('Warning!'),
                        'message': msg % partner.zip,
                    }
                else:
                    # properly format the entered postcode
                    partner.zip = postcode.compact(partner.zip)

        return {'warning': warning, }
