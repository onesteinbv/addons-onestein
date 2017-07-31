# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def create(self, vals):
        if vals.get('tag_ids', False) and vals.get('partner_id', False):
            categ_list = vals['tag_ids'][0][2]
            categs = self.env['crm.lead.tag'].browse(categ_list)

            customer_interests = []
            partner = self.env['res.partner'].browse(vals['partner_id'])
            if partner.parent_id:
                partner = partner.parent_id
            for interest in partner.interest_ids:
                if interest.name not in customer_interests:
                    customer_interests.append(interest.name)

            categ_names = []
            categ_color = {}
            for categ in categs:
                if categ.name not in categ_names:
                    categ_names.append(categ.name)
                    categ_color[categ.name] = categ.color

            new_interests = set(categ_names) - set(customer_interests)
            for name in new_interests:
                Interest = self.env['res.partner.interest']
                interest = Interest.search(
                    [('name', '=', name)], limit=1)
                if not interest:
                    interest = Interest.sudo().create(
                        {'name': name,
                         'color': categ_color[name]})
                partner.interest_ids += interest

        return super(CrmLead, self).create(vals)

    @api.multi
    def write(self, vals):
        for lead in self:
            if vals.get('tag_ids', False) or vals.get('partner_id', False):
                categs = lead.tag_ids
                if 'tag_ids' in vals and vals['tag_ids']:
                    categ_list = vals['tag_ids'][0][2]
                    categs = self.env['crm.lead.tag'].browse(categ_list)

                customer_interests = []
                partner = lead.partner_id
                if 'partner_id' in vals:
                    Partner = self.env['res.partner']
                    partner = Partner.browse(vals['partner_id'])
                if partner:
                    if partner.parent_id:
                        partner = partner.parent_id
                    for interest in partner.interest_ids:
                        if interest.name not in customer_interests:
                            customer_interests.append(interest.name)

                    categ_names = []
                    categ_color = {}
                    for categ in categs:
                        if categ.name not in categ_names:
                            categ_names.append(categ.name)
                            categ_color[categ.name] = categ.color

                    new_interests = set(categ_names) - set(customer_interests)
                    for name in new_interests:
                        Interest = self.env['res.partner.interest']
                        interest = Interest.search(
                            [('name', '=', name)], limit=1)
                        if not interest:
                            interest = Interest.sudo().create(
                                {'name': name,
                                 'color': categ_color[name]})
                        if partner:
                            partner.interest_ids += interest

        return super(CrmLead, self).write(vals)
