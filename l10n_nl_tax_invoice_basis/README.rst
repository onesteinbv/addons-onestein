.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=====================================
NL Tax Invoice Basis (Factuurstelsel)
=====================================

In the Netherlands, two types of accounting systems are allowed:

* Kasstelsel
* Factuurstelsel

By installing this module, you have the option to adopt the *Factuurstelsel* system for your Company in Odoo.
It means that, when validating an invoice, the system uses the invoice date instead of accounting date to determine the date of the move line for tax lines.
See https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aangifte_doen_en_betalen/bereken_het_bedrag/hoe_berekent_u_het_btw_bedrag/factuurstelsel

Without this module installed for example, when you use an accounting date with vendor invoices, the *Generic TAX reports* and the *Aangifte omzetbelasting* show the VAT in the wrong period/date.
So this module is meant to fill the gap between the standard Odoo way and the *Factuurstelsel* system, commonly used in the Netherlands.

The *Kasstelsel* system instead is provided by the standard Odoo module ``account_tax_cash_basis``.
Find more information about the kasstelsel system in: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aangifte_doen_en_betalen/bereken_het_bedrag/hoe_berekent_u_het_btw_bedrag/kasstelsel/kasstelsel


Installation
============

Install this module if you want to enable the *Factuurstelsel* system for your Company.

If you want to adopt the *Kasstelsel* system instead, consider to install the standard Odoo module ``account_tax_cash_basis``.


Configuration
=============

To enable the factuurstelsel, you need to:

#. Open your Company form and set its Country to ``Netherlands``.
#. Go to ``Invoicing -> Configuration -> Settings``, enable ``NL Tax Invoice Basis (Factuurstelsel)`` and ``Apply``.

In a multi-company environment, repeat the above steps for all the companies for which you want to enable the factuurstelsel.

Usage
=====

As an example, a use case of this module could be:

#. Create a Vendor Bill (Purchase Invoice) and set Accounting Date in a period different than the one of the invoice date (for example, the invoice date = 14-aug and the accounting date = 14-jul).
#. Generate your VAT statement report, it will be computed according to the factuurstelsel.

Known issues / Roadmap
======================

* This module extends the OCA module ``account_tax_balance``: only the TAX reports made with modules depending on ``account_tax_balance`` will comply with Factuurstelsel. Standard Odoo TAX reports are actually not compliant with Factuurstelsel.

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

* Dennis Sluijk <d.sluijk@onestein.nl>
* Andrea Stirpe <a.stirpe@onestein.nl>

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
