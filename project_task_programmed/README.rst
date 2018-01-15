.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

========================
Task Reminder Programmed
========================

Create automatically tasks as a reminder for any document (model) based on a date field.
The module is meant to remind (for example) a deadline by creating a task instead of an event.

If you want to plan the date when a new task will be created, based on a date of your document,
you should specify how much days in advance the task should be created.
Any date field can be used, for example a field that specifies a nearing deadline.

Let's say you have a generic object with deadline (or expiring date, or whatever date you prefer): 2016/04/01;
it doesn't matter whether the object is an invoice, an order, a task, an issue, etc...
Then with this module you can schedule that a new task will be created automatically one month before (2016/03/01).


Configuration
=============

By default, a cron job named "Create alert tasks" will be created while installing this module.
This cron job can be found in:

	**Settings > Technical > Automation > Scheduled Actions**

This job runs daily by default.


Usage
=====

To use this functionality, you need to:

#. Create a project to which the new tasks will be related.
#. Go to the Task Alerts Configuration (Project > Configuration > Task Alerts) and create a new record.
#. Add a name, a description of the task, who the task will be assigned to, etc...

The cron job will do the rest.

If you want to create the tasks manually, click on the button "Create Alerts"
in the Task Alerts Configuration form. This functionality is only
available for group Technical Features.



Credits
=======

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
