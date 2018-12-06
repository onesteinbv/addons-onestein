from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    show_christmas_light = fields.Boolean(
        string='Show Lights'
    )
