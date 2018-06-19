.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

========================
Directory Files Download
========================

View and download the files contained in a directory on the server.

This functionality can have impacts on the security of your system,
since it allows to download the content of a directory.
Be careful when choosing the directory!

Notice that, for security reasons, files like symbolic links
and up-level references are ignored.

Installation
============

To install this module, you need to:

#. Just install the module


Configuration
=============

To configure this module, you need to:

#. Set the group "Download files of directory" for the users who need this functionality.


Usage
=====

To use this module, you need to:

#. Go to Settings -> Downloads -> Directory Content
#. Create a record specifying Name and Directory of the server
#. Save; a list of files contained in the selected directory is displayed
#. Download the file you need
#. In case the content of the directory is modified, refresh the list by clicking the button on the top-right of the form

Credits
=======

Contributors
------------

* Andrea Stirpe <a.stirpe@onestein.nl>
