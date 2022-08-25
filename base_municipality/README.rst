=================
Base Municipality
=================

This module introduces a new "Municipality" field on company and partner
records, to be used as complement to all other address fields (e.g.: country,
state, zip, city, street, ...).

A municipality has a name and a code, and it is always a smaller administrative
division than a state, to which it belongs.
In no case two different municipalities with the same code can exist within the
same state.


Configuration
=============

To create new municipalities, you can:

* Go to "Contacts" -> "Configuration" -> "Localization" -> "Municipalities"
* Create a new record, filling-in the required fields;

This module comes pre-loaded with all Dutch municipalities, updated to July 2022.


Credits
=======

Authors
~~~~~~~

* Onestein

Contributors
~~~~~~~~~~~~

* Antonio Esposito <a.esposito@onestein.nl>
