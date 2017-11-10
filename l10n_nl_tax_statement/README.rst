.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=========================
Netherlands BTW Statement
=========================

This module provides you with the Tax Statement in the Dutch format.

Use this module in combination with module ``l10n_nl_tax_invoice_basis`` if you want to adopt the *Factuurstelsel* system for your Company.

Installation
============

* This module depends from module ``account_tax_balance`` available at https://github.com/OCA/account-financial-reporting.
* This module also depends from module date_range that is supported as of postgresql 9.2 or later versions.

Configuration
=============

This module makes use of the tax tags (eg.: 1a, 1b, 1c, 1d, 2a...) as prescribed by the Dutch tax laws.

If the default Odoo Dutch chart of accounts is installed (module ``l10n_nl``) then these tags are automatically present in the database.
If this is the case, go to menu: `Invoicing -> Configuration -> Accounting -> NL BTW Tags`, and check that the tags are correctly set; click Apply to confirm.

If a non-standard chart of accounts is installed, you have to manually create the tax tags and properly set them into the tax definition.
After that, go to go to menu: `Invoicing -> Configuration -> Accounting -> NL BTW Tags`, and manually set the tags in the configuration form; click Apply to confirm.

If your Company adopts the *Factuurstelsel* system for the accounting, also install the module ``l10n_nl_tax_invoice_basis``
(for more information about the installation and configuration of that module, check the README file).

Usage
=====

To create a statement you need to:

#. Verify that you have enough permits. You need to belong at least to the Accountant group.
#. Go to the menu: `Invoicing -> Reports > Taxes Balance > NL BTW Statement`
#. Create a statement, providing a name and specifying start date and end date
#. Press the Update button to calculate the report: the report lines will be displayed in the tab `Statement`
#. Manually enter the BTW amounts of lines '5d', '5e', '5f' (in Edit mode, click on the amount of the line to be able to change it)
#. Press the Post button to set the status of the statement to Posted; the statements set to this state cannot be modified

To add past undeclared invoices:

#. Open the tab `Past Undeclared Invoices`, available when the statement is in status Draft.
#. Set an initial date (field From Date) from which the past undeclared invoices will be displayed.
#. One by one, add the displayed undeclared invoices, by clicking on the `Add Invoice` button present in each line.
#. Press the Update button in order to recompute the statement lines.

Extra info about the workflow:

#. If you need to recalculate or modify or delete a statement already set to Posted status you need first to set it back to Draft status: press the button Reset to Draft
#. Instead, if you send the statement to the Tax Authority, you may want to avoid that the statement is set back to Draft: to avoid this, press the button Final. If you then confirm, it will be not possible to modify this Statement or reset it back to draft anymore.

Printing a FDF report:

#. If you need to print the report in PDF, open a statement form and click: `Print -> NL Tax Statement`


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/176/11.0


Known issues / Roadmap
======================

* Exporting in SBR/XBLR format not yet available

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n-netherlands/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
* Antonio Esposito <a.esposito@onestein.nl>

Do not contact contributors directly about support or help with technical issues.

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
