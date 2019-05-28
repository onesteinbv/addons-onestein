# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import ldap

from odoo import models


class ResCompanyLdap(models.Model):
    _inherit = 'res.company.ldap'

    def connect(self, conf):
        """
        Overrides the connect() method defined in module auth_ldap

        Connect to an LDAP server specified by an ldap
        configuration dictionary.

        :param dict conf: LDAP configuration
        :return: an LDAP object
        """

        uri = 'ldap://%s:%d' % (conf['ldap_server'],
                                conf['ldap_server_port'])

        connection = ldap.initialize(uri)

        # Disable referrals
        connection.set_option(ldap.OPT_REFERRALS, 0)

        if conf['ldap_tls']:
            connection.start_tls_s()
        return connection
