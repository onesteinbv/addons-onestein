.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
Account Multicompany Fullname
=============================

Within a Multicompany environment, some of the models of accounting
usually belong to a particular company.
For example, an account record (of model account.account) is per company
and its field 'company_id' refers to the Company which the record belongs to.

By installing this module, while selecting one record, its name
is enriched by displaying also the name of the related company.
This is done by extending the name_get() method.

The name_get() method is extended for the following models:
* account.account
* account.analytic.account
* account.fiscal.position
* account.journal
* account.tax
* account.tax.code


Credits
=======


Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
