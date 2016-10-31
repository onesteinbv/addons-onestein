.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Restrict automatic emails to partner
====================================

This module allows to configure the default value of the field "Opt-Out" while creating a new Partner.
The configuration is per-company, allowing different settings in a multi-company environment.

In standard Odoo, that field is defined in the module mail and its default value is False.

As stated in the help comment for the field (Odoo code, module email_template):
`
    help="If opt-out is checked, this contact has refused to receive emails for mass mailing and marketing campaign. "
`

If "Opt-Out" is True, newly created partners by default will not receive marketing emails or other kind of automated emails.


Configuration
=============

To configure this module, you need to:

#. Go to the Settings main menu and open the General Settings form;
#. check the field 'Default Opt-out for partners';
#. by default its value is True: new partners by default will not receive automatic emails;
#. set the value to False to allow new created partners to receive automatic emails by default.


Usage
=====

To use this module, you need to:

#. Create a Partner
#. check the Opt-out field in the Partner form
