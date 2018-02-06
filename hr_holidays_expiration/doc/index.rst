=================================
Holidays expiration documentation
=================================

Location:
---------

Leaves > My Leaves > Allocation Request > Tab "Expiration"


Test scenario:
--------------
 
1. Create multiple holiday allocation with different expiration dates 
2. Create leave requests and check allocation consumption. First expiring allocation should be consumed.


The new version contains the following changes/modifications:
-------------------------------------------------------------
 
1. Removed the following fields (full Validity field group) from the leave type:
	expirable, validity in Month, notify expiration via email, notify period, Notify email template, expired email template
2. Added Notify email template, expired email template to the Company configuration form
3. When creating a leave allocation the Notify email template, the default expired email template is copied from the Company.
