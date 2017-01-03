# -*- coding: utf-8 -*-
# Copyright (c) 2009-2016 Noviat nv/sa (www.noviat.com)
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Journal Items Search Cost Center',
    'version': '8.0.0.0.1',
    'license': 'AGPL-3',
    'author': 'ICTSTUDIO',
    'category': 'Cost Center',
    'depends': [
        'account_move_line_search_extension',
        'account_cost_center',
    ],
    'data': [
        'views/account_assets_backend.xml',
    ],
    'qweb': [
        'static/src/xml/account_move_line_search_cost_center.xml',
    ],
}
