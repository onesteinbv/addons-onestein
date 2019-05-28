.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Disable LDAP referrals
======================

This module sets the OPT_REFERRALS flag of the ldap connection to 0 while connecting to an LDAP server.

In standard Odoo, the OPT_REFERRALS flag is simply not set, so that its value is the one set by default within the ldap library.
In some cases, this causes Odoo hanging while binding the dn.


Configuration
=============

To configure this module, you need to:

#. No configuration needed.


Usage
=====

To use this module, you need to:

#. Login with an ldap user



Credits
=======


Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
