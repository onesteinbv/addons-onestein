from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    show_christmas_snowflakes = fields.Boolean(
        string='Show Snowflakes'
    )
