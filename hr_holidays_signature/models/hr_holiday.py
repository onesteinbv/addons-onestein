from openerp import api, fields, models, _

class Holiday(models.Model):
    _inherit = 'hr.holidays'
    
    manager_signature = fields.Binary('Signature manager')