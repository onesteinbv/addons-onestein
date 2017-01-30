.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================
HR Employee Holidays
====================

This module just adds field holiday_ids to Employee.
That field is missing in Odoo standard but is very
helpful when developing multiple features that require
the same field.

By installing this module only, not any functionality will be added to your system.
This module is meant to be a base module to be extended by modules that need
the field holiday_ids of Employee.
This way, we avoid that multiple modules create the same field, avoiding
conflicts causing confusion.


Credits
=======

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>


