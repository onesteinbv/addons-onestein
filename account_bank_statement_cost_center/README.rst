.. image:: https://img.shields.io/badge/license-AGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL-3

========================================
Encode Bank Statements with Cost Centers
========================================

Adds the Cost Center to the Bank Statement.

Accounting entries generated from the Bank Transactions will be handled as follows:

- The entry representing the money in/out will be set to the Cost Center of the Bank Statement.
- The counterparty entry/entries will be defaulted to the COst Center of the Bank Statement.
  This default can be changed manually via the "reconcile" widget