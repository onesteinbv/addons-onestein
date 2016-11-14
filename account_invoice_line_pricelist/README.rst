
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================
Account Invoice Line Pricelist
==============================

By installing this module, on customer/sale invoice lines the unit price will
be calculated based on the Price List set for the Invoice. If no Price List is
set on the invoice, then it will be calculated based on the Price List set for
the Customer.

By default, in the standard Odoo, the method 'product_id_change' of model
'account.invoice.line' doesn't take in consideration the pricelist assigned
to a customer when calculating the unit price of customer/sale invoice.
Moreover, in the standard Odoo, the model 'account.invoice' hasn't a
pricelist related field.

For invoices created from sale orders, product prices are already based on
price lists. This is the standard behavior on Odoo. Only for the invoices
created manually, the pricelist is not take in consideration.
This module aims to fix this behavior.

The same functionality, as described above, is provided for sale refunds.

Configuration
=============

No special configuration is needed.


Usage
=====

To use this module, you need to:

#. Set a price list for a Customer
#. Create a sale invoice for that Customer
#. On invoice lines, add some products (of which price is defined in price list)
#. Check whether the unit prices of the products are set accordingly to the price list


Credits
=======

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
* Antonio Esposito <a.esposito@onestein.nl>
