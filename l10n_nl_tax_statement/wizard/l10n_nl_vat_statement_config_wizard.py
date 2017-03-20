# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class VatStatementConfigWizard(models.TransientModel):
    _name = 'l10n.nl.vat.statement.config.wizard'

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

    @api.model
    def default_get(self, fields_list):
        defaults = super(VatStatementConfigWizard, self).default_get(fields_list)

        company_id = self.env.user.company_id.id
        config = self.env['l10n.nl.vat.statement.config'].search([
            ('company_id', '=', company_id)], limit=1
        )
        if config:
            defaults.setdefault('tag_1a_omzet', config.tag_1a_omzet.id)
            defaults.setdefault('tag_1a_btw', config.tag_1a_btw.id)
            defaults.setdefault('tag_1b_omzet', config.tag_1b_omzet.id)
            defaults.setdefault('tag_1b_btw', config.tag_1b_btw.id)
            defaults.setdefault('tag_1c_omzet', config.tag_1c_omzet.id)
            defaults.setdefault('tag_1c_btw', config.tag_1c_btw.id)
            defaults.setdefault('tag_1d_omzet', config.tag_1d_omzet.id)
            defaults.setdefault('tag_1d_btw', config.tag_1d_btw.id)
            defaults.setdefault('tag_1e_omzet', config.tag_1e_omzet.id)
            defaults.setdefault('tag_2a_omzet', config.tag_2a_omzet.id)
            defaults.setdefault('tag_2a_btw', config.tag_2a_btw.id)
            defaults.setdefault('tag_3a_omzet', config.tag_3a_omzet.id)
            defaults.setdefault('tag_3b_omzet', config.tag_3b_omzet.id)
            defaults.setdefault('tag_3c_omzet', config.tag_3c_omzet.id)
            defaults.setdefault('tag_4a_omzet', config.tag_4a_omzet.id)
            defaults.setdefault('tag_4a_btw', config.tag_4a_btw.id)
            defaults.setdefault('tag_4b_omzet', config.tag_4b_omzet.id)
            defaults.setdefault('tag_4b_btw', config.tag_4b_btw.id)
            defaults.setdefault('tag_5b_btw', config.tag_5b_btw.id)
            return defaults

        is_l10n_nl_coa = self.env.ref('l10n_nl.l10nnl_chart_template', False)
        company_coa = self.env.user.company_id.chart_template_id
        if company_coa == is_l10n_nl_coa:
            defaults.setdefault('tag_1a_omzet', self.env.ref('l10n_nl.tag_nl_03').id)
            defaults.setdefault('tag_1a_btw', self.env.ref('l10n_nl.tag_nl_20').id)
            defaults.setdefault('tag_1b_omzet', self.env.ref('l10n_nl.tag_nl_05').id)
            defaults.setdefault('tag_1b_btw', self.env.ref('l10n_nl.tag_nl_22').id)
            defaults.setdefault('tag_1c_omzet', self.env.ref('l10n_nl.tag_nl_06').id)
            defaults.setdefault('tag_1c_btw', self.env.ref('l10n_nl.tag_nl_23').id)
            defaults.setdefault('tag_1d_omzet', self.env.ref('l10n_nl.tag_nl_07').id)
            defaults.setdefault('tag_1d_btw', self.env.ref('l10n_nl.tag_nl_24').id)
            defaults.setdefault('tag_1e_omzet', self.env.ref('l10n_nl.tag_nl_08').id)
            defaults.setdefault('tag_2a_omzet', self.env.ref('l10n_nl.tag_nl_10').id)
            defaults.setdefault('tag_2a_btw', self.env.ref('l10n_nl.tag_nl_27').id)
            defaults.setdefault('tag_3a_omzet', self.env.ref('l10n_nl.tag_nl_12').id)
            defaults.setdefault('tag_3b_omzet', self.env.ref('l10n_nl.tag_nl_13').id)
            defaults.setdefault('tag_3c_omzet', self.env.ref('l10n_nl.tag_nl_14').id)
            defaults.setdefault('tag_4a_omzet', self.env.ref('l10n_nl.tag_nl_16').id)
            defaults.setdefault('tag_4a_btw', self.env.ref('l10n_nl.tag_nl_29').id)
            defaults.setdefault('tag_4b_omzet', self.env.ref('l10n_nl.tag_nl_17').id)
            defaults.setdefault('tag_4b_btw', self.env.ref('l10n_nl.tag_nl_30').id)
            defaults.setdefault('tag_5b_btw', self.env.ref('l10n_nl.tag_nl_33').id)
        return defaults

    @api.multi
    def execute(self):
        self.ensure_one()

        company_id = self.env.user.company_id.id
        statement_config = self.env['l10n.nl.vat.statement.config'].search([
            ('company_id', '=', company_id)], limit=1
        )
        if not statement_config:
            statement_config = self.env['l10n.nl.vat.statement.config'].create({
                'company_id': company_id
            })
        statement_config.write({
            'company_id': company_id,
            'tag_1a_omzet': self.tag_1a_omzet.id,
            'tag_1a_btw': self.tag_1a_btw.id,
            'tag_1b_omzet': self.tag_1b_omzet.id,
            'tag_1b_btw': self.tag_1b_btw.id,
            'tag_1c_omzet': self.tag_1c_omzet.id,
            'tag_1c_btw': self.tag_1c_btw.id,
            'tag_1d_omzet': self.tag_1d_omzet.id,
            'tag_1d_btw': self.tag_1d_btw.id,
            'tag_1e_omzet': self.tag_1e_omzet.id,
            'tag_2a_omzet': self.tag_2a_omzet.id,
            'tag_2a_btw': self.tag_2a_btw.id,
            'tag_3a_omzet': self.tag_3a_omzet.id,
            'tag_3b_omzet': self.tag_3b_omzet.id,
            'tag_3c_omzet': self.tag_3c_omzet.id,
            'tag_4a_omzet': self.tag_4a_omzet.id,
            'tag_4a_btw': self.tag_4a_btw.id,
            'tag_4b_omzet': self.tag_4b_omzet.id,
            'tag_4b_btw': self.tag_4b_btw.id,
            'tag_5b_btw': self.tag_5b_btw.id,
        })
