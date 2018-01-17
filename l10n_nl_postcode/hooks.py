# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api

try:
    from stdnum.nl import postcode
except ImportError:
    logging.getLogger('odoo.addons.l10n_nl_postcode').debug(
        'Cannot `import stdnum.nl.postcode`.')


def post_init_hook(cr, registry):
    """
    Post-install script. Properly format all postcodes
    already present on partners while installing the module.
    """
    logging.getLogger('odoo.addons.l10n_nl_postcode').info(
        'Migrating existing postcodes')

    env = api.Environment(cr, SUPERUSER_ID, {})
    partners = env['res.partner'].with_context(active_test=False).search([
        ('zip', '!=', False),
        ('country_id', '=', env.ref('base.nl').id),
    ])

    for partner in partners:
        # check whether postcode is valid, if so then format postcode
        #  otherwise ignore
        if partner.zip and postcode.is_valid(partner.zip):
            partner.zip = postcode.compact(partner.zip)
