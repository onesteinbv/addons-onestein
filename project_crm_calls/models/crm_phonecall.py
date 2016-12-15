# -*- coding: utf-8 -*-
# Copyright 2015 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields
from openerp.exceptions import Warning
from openerp.tools.translate import _


class CrmPhonecall(models.Model):

    _inherit = 'crm.phonecall'

    is_project_call = fields.Boolean('Is Project Call')
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        domain=[('state', 'not in', ['cancelled', 'close']),
                ('use_issues', '=', True)
                ]
    )
    is_processed = fields.Boolean('Is Processed')
    project_issue_id = fields.Many2one('project.issue', string='Issue')

    @api.multi
    def action_button_convert2issue(self):
        issue = None
        for call in self:
            if not call.project_id:
                raise Warning(
                    _('No project selected, please select a project.')
                )
            call.is_processed = True
            issue = call.project_issue_id
            analytic_account = call.project_id.analytic_account_id
            if not issue:
                partner_id = call.partner_id and call.partner_id.id or None
                vals = {
                    'name': call.name,
                    'project_id': call.project_id.id,
                    'analytic_account_id': analytic_account.id,
                    'call_id': call.id,
                    'active': True,
                    'partner_id': partner_id,
                    'is_processed': True,
                }
                issue = self.env['project.issue'].create(vals)
                call.project_issue_id = issue
        if not issue:
            raise Warning(
                _('An unhandled exception was raised '
                  'while converting to an issue.')
            )

        form_view = call.env.ref('project_issue.project_issue_form_view')

        return {
            'name': _('Convert Project to Issue'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.issue',
            'view_id': form_view.id,
            'res_id': issue.id,
        }

    def convert_opportunity(
            self, cr, uid, ids, opportunity_summary=False, partner_id=False,
            planned_revenue=0.0, probability=0.0, context=None):
        partner = self.pool.get('res.partner')
        opportunity = self.pool.get('crm.lead')
        opportunity_dict = {}
        default_contact = False
        for call in self.browse(cr, uid, ids, context=context):
            if not partner_id:
                partner_id = call.partner_id and call.partner_id.id or False
            if partner_id:
                address_id = partner.address_get(
                    cr, uid, [partner_id])['default']
                if address_id:
                    default_contact = partner.browse(
                        cr, uid, address_id, context=context)
            section_id = call.section_id and call.section_id.id or False
            opportunity_id = opportunity.create(
                cr, uid,
                {'name': opportunity_summary or call.name,
                 'planned_revenue': planned_revenue,
                 'probability': probability,
                 'partner_id': partner_id or False,
                 'mobile': default_contact and default_contact.mobile,
                 'section_id': section_id,
                 'description': call.description or False,
                 'priority': call.priority,
                 'type': 'opportunity',
                 'phone': call.partner_phone or False,
                 'email_from': default_contact and default_contact.email,
                 })
            vals = {
                'partner_id': partner_id,
                'opportunity_id': opportunity_id,
                'state': 'done',
                'is_processed': True,
            }
            self.write(cr, uid, [call.id], vals, context=context)
            opportunity_dict[call.id] = opportunity_id
        return opportunity_dict
