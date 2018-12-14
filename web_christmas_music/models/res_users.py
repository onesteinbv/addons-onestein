from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    play_christmas_music = fields.Boolean(
        string='Play Christmas Music'
    )

    def __init__(self, pool, cr):
        init_res = super(ResUsers, self).__init__(pool, cr)

        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(['play_christmas_music'])
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(['play_christmas_music'])

        return init_res
