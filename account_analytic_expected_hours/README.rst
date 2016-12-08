.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Account Analytic Expected Hours
===============================

By installing this module the user will be able to be warned
on writing hours while reaching the expected hours.

If configured, the user could be also blocked on writing hours
while reaching the expected hours.


Configuration
-------------

*Percentage*
On the contract, set a percentage field on which the user
writing hours is to be alerted that a block is near.

*Block and alert*
The block option is a selection list, with three values: No block (which
acts as an unchecked check-box), Block (which acts as checked check-box) and Alert but don't block.
The latter raises a similar dialog box as the Block option, however, it's allowed to submit the
time-sheet.

*Allowed Period*
An allowed period exists out of a start date and end date. When they are set, it's possible to
write hours on the analytic account after the start date and before the end date. If the end date is not set, it
is possible to write hours on all days before the end date and on the end date, likewise if the start date is
not set, it is possible to write hours on the start date and any day thereafter.
Both dates are inclusive.


Usage
-----

To use this module, you need to:

#. Create or modify timesheet lines in order to exceed the defined limits.


Credits
=======

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
