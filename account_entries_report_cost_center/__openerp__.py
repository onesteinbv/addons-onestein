# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Accounting Entries Report - Cost Center",
    "version": "8.0.1.0.0",
    "author": "ICTSTUDIO, "
              "Eficent, Serpent Consulting Services Pvt. Ltd., "
              "Odoo Community Association (OCA)",
    "website": "http://www.ictstudio.eu",
    "category": "Generic",
    "depends": ["account_entries_report_hooks",
                'account_cost_center'],
    "license": "AGPL-3",
    "data": [
        'views/account_entries_report_view.xml'
    ],
}
