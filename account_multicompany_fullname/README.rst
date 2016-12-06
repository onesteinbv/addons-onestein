.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
Account Multicompany Fullname
=============================

Within a Multicompany environment, the records of some accounting models
belong to a certain company. For example, one account (record of
model account.account) is defined per company: its field 'company_id' refers
to one of the Companies present in the system.

By installing this module, while selecting one of such records, its name
also contains the name of its related company.
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
