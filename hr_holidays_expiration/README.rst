
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

The persons responsible for managing leaves are informed automatically by email.



Configuration
-------------

To use this module you have to set an expiration date on the leave allocations.
Please add the period in which the leave is valid.

When a manager want to be informed about a leave which is about to expire, tick the "Notify Expiration via Email" box.
Apply the period in days and the email templates.

A cron job called "Set expired holidays" will be executed every day.
This can be checked in the Setting menu:

    **Automation > Scheduled actions**

|



Test scenario
-------------


1. Create multiple holiday allocation with different expiration dates
2. Create leave requests and check allocation consumption. First expiring allocation should be consumed.



Contact us
----------

When you have any remark about this module, please let us know on http://www.onestein.eu/feedback


