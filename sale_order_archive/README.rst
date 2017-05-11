.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
Sale Order Archive
==================

On a system with a high volume of sales, the number of sale orders displayed in the list view can become huge.
This module allows to archive Sale Orders that are in status Locked or Cancelled.

If a sale order is archived, it will be hidden from the sale orders list view.

This module only depends on module sale, but it could be used in combination with OCA module 'record_archiver' in order to automatically archive old sale orders.


Installation
============

To install this module, just use the standard procedure.

Configuration
=============

No configuration needed.

Usage
=====

To archive sale orders, you need to:

#. Open the tree view of sale orders.
#. Select a sale order (in status Locked or Cancelled) you want to archive.
#. Position your mouse cursor on the Active smart button and click it.
#. The sale order is now archived.

To unarchive sale orders, you need to:

#. Open the tree view of sale orders.
#. In the filter box select the Archived filter. The list of archived sale orders will be displayed.
#. Select the sale order (in status Locked or Cancelled) you want to unarchive.
#. Position your mouse cursor on the Archived smart button and click it.
#. The sale order is now unarchived.


Credits
=======

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
