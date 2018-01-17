# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)
try:
    from stdnum.nl import postcode
except ImportError:
    _logger.debug('Cannot `import stdnum.nl.postcode`.')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _get_warning(self):
        self.ensure_one()
        msg = _('The Postcode you entered (%s) is not valid.')
        warning = {
            'title': _('Warning!'),
            'message': msg % self.zip,
        }
        return warning

    @api.multi
    def _do_format(self):
        self.ensure_one()
        # properly format the entered postcode
        self.zip = postcode.compact(self.zip)

    @api.multi
    def _check_country(self):
        self.ensure_one()
        country = self.country_id
        if not country or country != self.env.ref('base.nl'):
            return False
        return True

    @api.multi
    @api.onchange('zip')
    def onchange_zip_l10n_nl_postcode(self):
        if self.env.context.get('skip_postcode_check'):
            return

        if self.zip and self._check_country():
            # check is valid, otherwise display a warning
            if postcode.is_valid(self.zip):
                self._do_format()
            else:
                warning = self._get_warning()
                return {'warning': warning, }
