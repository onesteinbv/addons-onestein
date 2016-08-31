.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Restrict automatic emails to partner
====================================

This module sets the default value of the field "Opt-Out" to True while creating a Partner.
In standard Odoo, that field is defined in the module email_template and its default value is False.

As stated in the help comment for the field (Odoo code, module email_template):
`
    help="If opt-out is checked, this contact has refused to receive emails for mass mailing and marketing campaign. "
`

By installing this module, newly created partners by default will not receive marketing emails or other kind of automated emails.


Configuration
=============

To configure this module, you need to:

#. No configuration needed.


Usage
=====

To use this module, you need to:

#. Create a Partner
