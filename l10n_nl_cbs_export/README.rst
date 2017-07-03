.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================
Dutch CBS Export
================

CBS = Dutch Bureau of Statistics (Centraal Bureau voor de statistiek)

When you export products within the EU you have to report those exports to the Dutch CBS.
This module will provide a export CSV file which you can upload on the CBS website. The CSV
file is automatically created every month trough a cron job.


Installation
============

To install this module, you need to:
#. Install the module
#. This module depends on the Odoo module report_intrastat, for the intrastat code and countries for intrastat reporting


Configuration
=============

To configure this module, you need to:

#. Go to Sales > Configuration > Countries and check if all EU countries are checked as 'Intrastat member"
#. Set the Intrastat code on the products
#. Go to Technical Settings > Scheduled Actions and set the Cron "Generate CBS Export File" job on the monthly date you want to have the CSV file

Usage
=====

To use this module, you need to:

#. Go to Accounting > Reports > Export files > CBS Export (the user must belong to group "Accounting & Finance / Billing")
#. Download the created CSV file and upload in to the CBS website
#. The user belonging to group "Accounting & Finance / Adviser" can use the button "Manual CBS Export" to force a re-creation of the CSV file

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/176/10.0

Known issues / Roadmap
======================

* Only for export (sale invoices). Import (Vendor bills) is not implemented
* Only for "Intrahandel". That is export within the EU
* Field Transport "Vervoerwijze" is set hardcoded on 3. This is the most common used value.
* Field Statistic stelsel "Statistisch Stelsel" is set hardcoded on 00. This is the most common used value.
* Field Transaction "Transactie" is set hardcoded on 1. This is the most common used value.
* Field "Bijzondere maatstaf" is not yet implemented.

See documentation added to this module (doc folder) for further information about the layout and field values.

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

* Erwin van der Ploeg <erwin@odooexperts.nl>
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
