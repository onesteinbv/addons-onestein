.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
Web Tours Disabled
==================

**21 Dec 2016: This module is obsolete, superseded by OCA module "web_no_bubble" !**

This module disables (hides) the animations of the Odoo Web Tours.

In the standard Odoo there is already an UI option to disable the tour. It is
present in a menu item called "Consume Tours" and is available by enabling the
Developer mode. But such functionality requires some steps to be done by the user (admin).

For our Saas service we needed a way to disable the tour without any required
interaction by the user. This way, we don't need to instruct the user to disable the tour
manually, following the standard procedure. When we create a fresh database in our Saas,
the module web_tour_disabled in installed by default and the newly created admin user
is not annoyed by the tour tips.


Configuration
=============

To configure this module, you need to:

#. No configuration needed. Just install the module.

Credits
=======

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
