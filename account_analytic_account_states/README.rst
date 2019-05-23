.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================
Account Analytic Account State
==============================

By installing this module, it will introduce a state workflow for the analytic accounts.

The states introduced by this module are:

#. Draft: It's the starting state of an analytic account;
#. Waiting For Approval: The analytic account was submitted by the user. It can be approved or refused by a manager or reset back to draft;
#. Approved: The analytic account was approved by a manager. It can still be reset to draft;
#. Declined: The analytic account was refused by a manager. It can be reset to draft;
#. Expired: The analytic account ran into its end. It can be resubmitted in order to extend its duration;
#. Cancelled: The analytic account was cancelled. It's still possible to reset it to draft;

All the transitions between the states can be manually triggered by users with the right permissions.

N.B.: To properly work, this module needs to install the module account_analytic_account_accessibility which can also be found in this repository.

Configuration
=============

This module doesn't require further configurations than what already required to work with Analytic Accounts.

Usage
=====

To use this module, you need to:

#. Go to 'Accounting' - 'Configuration' - 'Analytic Accounting' - 'Analytic Accounts'
#. Select an already existing analytic account
#. According to its current state and to the user's permissions, it will possible to click on buttons in order to trigger state transitions.

The available buttons are:

#. Submit (only for users in group Technical Settings/Analytic Accounting): Draft -> Waiting for Approval
#. Cancel (only for users in group Technical Settings/Analytic Accounting): Draft -> Cancelled
#. Set to Expired (only for users in group Technical Settings/Analytic Account Manager): Draft, Waiting for Approval, Approved -> Expired
#. Approve (only for users in group Technical Settings/Analytic Account Manager): Waiting for Approval -> Approved
#. Decline (only for users in group Technical Settings/Analytic Account Manager): Waiting for Approval -> Declined
#. Resubmit (only for users in group Technical Settings/Analytic Accounting): Expired -> Waiting for Approval
#. Reset to Draft (only for users in group Technical Settings/Analytic Accounting): Cancel, Declined, Approved -> Draft

Credits
=======

Contributors
------------

* Antonio Esposito <a.esposito@onestein.nl>
* Andrea Stirpe <a.stirpe@onestein.nl>
