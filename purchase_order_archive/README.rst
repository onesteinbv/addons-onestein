.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Purchase Order Archive
======================

On a system with a high volume of purchases, the number of purchase orders displayed in the list view can become huge.
This module allows to archive Purchase Orders that are in status Locked or Cancelled.

If a purchase order is archived, it will be hidden from the purchase orders list view.

This module only depends on module purchase, but it could be used in combination with OCA module 'record_archiver' in order to automatically archive old purchase orders.


Installation
============

To install this module, just use the standard procedure.

Configuration
=============

No configuration needed.

Usage
=====

To archive purchase orders, you need to:

#. Open the tree view of purchase orders.
#. Select a purchase order (in status Locked or Cancelled) you want to archive.
#. Position your mouse cursor on the Active smart button and click it.
#. The purchase order is now archived.

To unarchive purchase orders, you need to:

#. Open the tree view of purchase orders.
#. In the filter box select the Archived filter. The list of archived purchase orders will be displayed.
#. Select the purchase order (in status Locked or Cancelled) you want to unarchive.
#. Position your mouse cursor on the Archived smart button and click it.
#. The purchase order is now unarchived.


Credits
=======

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
