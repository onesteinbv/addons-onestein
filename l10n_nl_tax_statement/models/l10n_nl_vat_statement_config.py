# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class VatStatementConfig(models.Model):
    _name = 'l10n.nl.vat.statement.config'

    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True
    )

    tag_1a_omzet = fields.Many2one('account.account.tag')
    tag_1a_btw = fields.Many2one('account.account.tag')
    tag_1b_omzet = fields.Many2one('account.account.tag')
    tag_1b_btw = fields.Many2one('account.account.tag')
    tag_1c_omzet = fields.Many2one('account.account.tag')
    tag_1c_btw = fields.Many2one('account.account.tag')
    tag_1d_omzet = fields.Many2one('account.account.tag')
    tag_1d_btw = fields.Many2one('account.account.tag')
    tag_1e_omzet = fields.Many2one('account.account.tag')
    tag_2a_omzet = fields.Many2one('account.account.tag')
    tag_2a_btw = fields.Many2one('account.account.tag')
    tag_3a_omzet = fields.Many2one('account.account.tag')
    tag_3b_omzet = fields.Many2one('account.account.tag')
    tag_3c_omzet = fields.Many2one('account.account.tag')
    tag_4a_omzet = fields.Many2one('account.account.tag')
    tag_4a_btw = fields.Many2one('account.account.tag')
    tag_4b_omzet = fields.Many2one('account.account.tag')
    tag_4b_btw = fields.Many2one('account.account.tag')
    tag_5b_btw = fields.Many2one('account.account.tag')
    tag_5b_btw_bis = fields.Many2one('account.account.tag')
