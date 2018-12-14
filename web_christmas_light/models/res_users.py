from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    show_christmas_light = fields.Boolean(
        string='Show Lights'
    )

    def __init__(self, pool, cr):
        init_res = super(ResUsers, self).__init__(pool, cr)

        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(['show_christmas_light'])
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(['show_christmas_light'])

        return init_res
