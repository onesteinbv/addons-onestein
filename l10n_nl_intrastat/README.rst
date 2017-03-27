.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================
Intrastat reporting (ICP) for the Netherlands
=============================================

Based on the OCA Intrastat framework, this module provides an
intrastat report for the Netherlands. Only generating the required data
for a manual declaration is supported. Message communication with the
tax authority has not yet been implemented.

The intrastat base module requires the country field required on
partner addresses. Selected countries are marked for inclusion in this report.

Amounts for products and services are reported separately. All services
are reported, regardless of the 'Accessory cost setting' which is used in
the French version of this report.

To exclude specific lines from the report, you can mark specific taxes
as such. If such a tax is applied to the line, the line will not be
included in the reported amounts.

Configuration
=============

To configure this module, you need to:

#. Configure the country of your company (NL)

Usage
=====

To use this module, you need to:

#. Have invoices to some partners in other EU countries
#. Go to Invoicing - Financial Reports - Intrastat - ICP report
#. Create a report, define a date range, press Update
#. Watch the ICP report values for this date range appear
#. Manually copy the values into your ICP tax entry

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/176/10.0

Known issues / Roadmap
======================

* The Dutch tax authority accepts an XML format, generate this to avoid manual processing.

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

* Therp BV
* Sunflower IT
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
