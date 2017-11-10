.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
Burgerservicenummer (BSN) for Partners
======================================

This module adds the BSN (Burgerservicenummer) field on partner forms.

The field is visible when the flag is_company is false.

A double check on the BSN is done when inserting/modifying its value:
 - validation of the BSN (check whether the format is correct);
 - check if another partner with the same BSN already exists.
In both cases, a non-blocking alert is shown.


Installation
============

The module depends on the external library 'python-stdnum'.

You can install that library by using pip:

* pip install python-stdnum


Configuration
=============

For security reasons the BSN number should be only visible to HR related roles.
Otherwise this will be in violation to the security framework of WBP regarding
the protection of persons info.

To be able to see the BSN number, give the proper permits to the user:

* User must belong to the "HR Officer" group


Usage
=====

To use this module, you need to:

* Open a form of a contact, eg.: a person (uncheck the flag "Is a Company?")
* Enter a BSN number

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/176/11.0


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n-netherlands/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
