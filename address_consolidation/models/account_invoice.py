# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import re
from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    invoice_partner_street = fields.Char('Street')
    invoice_partner_street2 = fields.Char('Street2')
    invoice_partner_zip = fields.Char('Zip', size=24)
    invoice_partner_city = fields.Char('City')
    invoice_partner_state_id = fields.Many2one(
        'res.country.state',
        string='State')
    invoice_partner_country_id = fields.Many2one(
        'res.country',
        string='Country')

    @api.multi
    def onchange_partner_id(
            self, type, partner_id, date_invoice=False, payment_term=False,
            partner_bank_id=False,  company_id=False):
        res = super(AccountInvoice, self).onchange_partner_id(
            type, partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id,
            company_id=company_id)

        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            res['value'].update({
                'invoice_partner_street': partner.street,
                'invoice_partner_street2': partner.street2,
                'invoice_partner_zip': partner.zip,
                'invoice_partner_city': partner.city,
                'invoice_partner_state_id': partner.state_id.id,
                'invoice_partner_country_id': partner.country_id.id,
            })
        return res

    @api.model
    def _prepare_refund(
            self, invoice, date=None, period_id=None, description=None,
            journal_id=None):
        values = super(AccountInvoice, self)._prepare_refund(
            invoice, date=date, period_id=period_id, description=description,
            journal_id=journal_id)

        values.update({
            'invoice_partner_street': invoice.invoice_partner_street,
            'invoice_partner_street2': invoice.invoice_partner_street2,
            'invoice_partner_zip': invoice.invoice_partner_zip,
            'invoice_partner_city': invoice.invoice_partner_city,
            'invoice_partner_state_id': invoice.invoice_partner_state_id.id,
            'invoice_partner_country_id': invoice.invoice_partner_country_id.id,
        })

        return values

    @api.multi
    def _display_invoice_partner_address(
            self, invoice, without_company=False, context=None):
        address_format = invoice.partner_id.country_id.address_format or \
            "%(street)s\n%(street2)s\n%(city)s %(state_code)s %(zip)s\n%(country_name)s"

        args = {
            'street': invoice.invoice_partner_street or '',
            'street2': invoice.invoice_partner_street2 or '',
            'zip': invoice.invoice_partner_zip or '',
            'city': invoice.invoice_partner_city or '',
            'company_name': invoice.partner_id.name or '',
            'state_code': invoice.invoice_partner_state_id.code or '',
            'state_name': invoice.invoice_partner_state_id.name or '',
            'country_code': invoice.invoice_partner_country_id.code or '',
            'country_name': invoice.invoice_partner_country_id.name or '',
        }

        if without_company:
            args['company_name'] = ''
        elif invoice.partner_id.parent_id:
            address_format = '%(company_name)s\n' + address_format

        res = address_format % args
        res = re.sub("\n\n|\n", "<br/>", res)
        return res
