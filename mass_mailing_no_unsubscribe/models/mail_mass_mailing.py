# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MailMassMailing(models.Model):
    _inherit = 'mail.mass_mailing'

    allow_unsubscribe = fields.Boolean('Allow Unsubscribe')
