# -*- coding: utf-8 -*-
# Copyright 2015 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProjectIssue(models.Model):

    _inherit = 'project.issue'

    call_id = fields.Many2one(
        'crm.phonecall',
        'Origin Call'
    )
    related_call_id = fields.Many2one(
        related='call_id',
        comodel_name='crm.phonecall',
        string='Origin Call'
    )
