# Copyright 2016-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Cost-Revenue Spread",
    "summary": "Spread costs and revenues over a custom period",
    "version": "11.0.2.3.0",
    "development_status": "Beta",
    "author": "Onestein",
    "maintainers": ["astirpe"],
    "license": "AGPL-3",
    "website": "https://github.com/OCA/account-financial-tools/",
    "category": "Accounting & Finance",
    "depends": [
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_invoice_line.xml",
        "views/account_invoice.xml",
        "data/spread_cron.xml",
        "templates/assets.xml",
    ],
    "installable": True,
}
