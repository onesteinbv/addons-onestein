====================
Office 365 Connector
====================

.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge2|

This module allows you to synchronize your Office 365 calendar with Odoo.

**Table of contents**

.. contents::
   :local:

Installation
============

For this module you need to install ``requests-oauthlib``.

Open the terminal and run: ``sudo pip3 install requests-oauthlib``

Configuration
=============

First you have to register your Odoo server with the Microsoft App Registration Portal:

#. Go to https://apps.dev.microsoft.com/;
#. under Converged applications click 'Add an app';
#. fill in any name e.g. 'My Odoo Server';
#. click 'Generate New Password' and store the password we will need it later;
#. click 'Add Platform' and select 'Web';
#. enter the redirect url e.g.: 'https://yourodooserver.com/office-365-oauth/success' replace 'yourodooserver.com' with the address of your Odoo server (note that your Odoo server has to be accessible via HTTPS);
#. add the following permissions: 'User.Read', 'Calendars.ReadWrite', and 'offline_access'.

It should look like this:

.. image:: https://raw.githubusercontent.com/onesteinbv/addons-onestein/12.0/connector_office_365/static/description/screenshot-setup.png
   :alt: Screenshot Microsoft App Registration Portal

Setup Odoo:

#. Go to Settings > General Settings;
#. fill the Client ID with the Client ID / Application ID from the Microsoft App Registration Portal;
#. put the password from before in Client Secret.


Usage
=====

To start synchronizing your calendar:

#. Go to Calendar;
#. click Sync with office 365;
#. you'll be redirected to the login page of Office 365;
#. login into you're account;
#. on completion you'll be redirected (if setup properly) back to your Odoo server.

The synchronization is personal per user.

Known issues / Roadmap
======================

* Synchronize contacts
* Synchronize files
* Synchronize notes

Credits
=======

Authors
~~~~~~~

* Onestein

Contributors
~~~~~~~~~~~~

* Dennis Sluijk <d.sluijk@onestein.nl>
* Guewen Baconnier <guewen.baconnier@camptocamp.com>
