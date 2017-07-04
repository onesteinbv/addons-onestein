.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
Project Issue Type
==================

This module adds a model 'project.issue.type' and a many2one field 'type'
in the project issue model. Both the model and the 'type' field are missing
in the standard Odoo.

This module is helpful when developing multiple features that require
the same field.

By installing this module, not any functionality will be added to your system.
This module is meant to be a base module to be extended with other modules that
need a field 'type' for the model 'project.issue'.
Is a way to avoid that multiple modules create the same field, that would cause
conflicts and confusion.


Usage
=====

To use this module, you need to:

#. Open an issue form and select its type.


Credits
=======

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
