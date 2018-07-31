.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
Dutch postcode validation for Partners
======================================

This module checks and validates the Dutch zip code (postcode) on partner forms.

* In case the postcode is not valid, a non-blocking alert is shown.
* In case the postcode is valid, it will be formatted in the form *1234 AB*.


Installation
============

The module depends on the external library 'python-stdnum'.

You can install that library by using pip:

* pip install python-stdnum

Usage
=====

To use this module, you need to:

* Open a form of a contact and set it as *Individual* (not a *Company*)
* Enter the country = Netherlands
* Enter a valid postcode: not any warning is displayed
* Enter a wrong postcode: a non-blocking warning is displayed

Credits
=======

Authors
~~~~~~~

* Onestein

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
