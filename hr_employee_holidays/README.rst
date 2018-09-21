.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

====================
HR Employee Holidays
====================

This module simply adds a holiday_ids field to the Employee model.
That field is missing in the standard Odoo but it turns very
useful when developing features requiring that field.

This way, we avoid that multiple modules create the same field, avoiding
conflicts that may cause confusion.

By installing this module, no new functionality will be added to your system.
This module is meant to be a technical module that must be extended by other modules.


Usage
=====


For example, my inheriting this module, this piece of code:

.. code-block:: python

   class HrEmployee(models.Model):
       _inherit = "hr.employee"

       def _my_employees_holidays(self):
           employee_ids = self.ids
           holidays = self.env['hr.holidays'].search([
               ('employee_id', 'in', employee_ids)
           ])
           return holidays

can be simply written as:

.. code-block:: python

   class HrEmployee(models.Model):
       _inherit = "hr.employee"

       def _my_employees_holidays(self):
           holidays = self.holidays_ids
           return holidays

Credits
=======

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
