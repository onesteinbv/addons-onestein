# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_hook(cr, pool):
    env = Environment(cr, SUPERUSER_ID, {})
    env['mail.followers']._align_followers(
        'project.project', 'account.analytic.account')
    env['mail.followers']._align_followers(
        'account.analytic.account', 'project.project')
