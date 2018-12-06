from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    play_christmas_music = fields.Boolean(
        string='Play Christmas Music'
    )
