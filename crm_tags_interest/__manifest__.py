# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CRM Tags Interest',
    'summary': 'Add interests to CRM leads and prospects',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Sales Management',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'crm',
        'sale',
        'sales_team',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/crm_lead.xml',
        'views/res_partner.xml',
        'views/res_partner_interest.xml',
        'menu_items.xml',
    ],
    'installable': True,
}
