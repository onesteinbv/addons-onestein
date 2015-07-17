# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ONESTEiN BV (<http://www.onestein.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import re

import logging
from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    invoice_partner_street = fields.Char('Street')
    invoice_partner_street2 = fields.Char('Street2')
    invoice_partner_zip = fields.Char('Zip', size=24)
    invoice_partner_city = fields.Char('City')
    invoice_partner_state_id = fields.Many2one('res.country.state', string='State')
    invoice_partner_country_id = fields.Many2one('res.country', string='Country')

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
                            payment_term=False, partner_bank_id=False, company_id=False):
        _logger.debug('ONESTEiN account_invoice onchange_partner_id')
        res = super(account_invoice, self).onchange_partner_id(
            type, partner_id, date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False
        )

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
    def _prepare_refund(self, invoice, date=None, period_id=None, description=None, journal_id=None):
        _logger.debug('ONESTEiN account_invoice _prepare_refund')
        values = super(account_invoice, self)._prepare_refund(invoice, date=None, period_id=None, description=None,
                                                              journal_id=None)

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
    def _display_invoice_partner_address(self, invoice, without_company=False, context=None):
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
