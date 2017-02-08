.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================
Holidays expiration
===================

This module adds the possibility to manage the expiration of the holidays including
the possibility to send a customizable warning email to the HR responsible.

In a multi-company environment, the expiry is set at the allocation request.
Then you can combine all holidays into one holiday leave type
regardless of what is the current Company (this is the standard behavior of Odoo).
This allows the end users to just have to select one type of holiday and the HR officer/manager
can set their different expiry types (eg.: statutory / non - statutory) per allocation.

The holiday allocations are consumed according first expiration first.




Test scenario:
1. Create multiple holiday allocation with different expiration dates
2. Create leave requests and check allocation consumption. First expiring allocation should be consumed.



The new version contains the following changes/modifications:
1. Removed the following fields (full Validity field group) from the leave type:
           expirable, validity in Month, notify expiration via email, notify period, Notify email template, expired email template
2. Added Notify email template, expired email template to the Company configuration form
3. When creating a leave allocation the Notify email template, the default expired email template is copied from the Company.

