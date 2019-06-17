=============================
Office 365 Connector - Leaves
=============================

.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge2|

This module extends the Office 365 connector to push employee leaves.

**Table of contents**

.. contents::
   :local:

Installation
============

The installation requirements are the same as Office 365 Connector.

Usage
=====

When a leave is approved for an employee, it is automatically pushed to the
Office365 calendar, provided that:

* the employee is a user as well
* the user authenticated herself with Office 365

If the user did not run the authentication, the event will not be pushed.
Instead, an activity will be added to the user asking to authenticate. Then a
button on the leave will allow to manually push the event.

Known issues / Roadmap
======================

Credits
=======

Authors
~~~~~~~

* Camptocamp

Contributors
~~~~~~~~~~~~

* Guewen Baconnier <guewen.baconnier@camptocamp.com>
