# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ONESTEiN BV (<http://www.onestein.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from openerp.osv import osv, fields
from openerp import tools

_logger = logging.getLogger(__name__)

class MassMailing(osv.Model):
    _name = 'mail.mass_mailing'
    _inherit = 'mail.mass_mailing'
    
    _columns = {
        'allow_unsubscribe': fields.boolean('Allow unsubscribe')
    }
  

class MailMail(osv.Model):
    _name = 'mail.mail'
    _inherit = 'mail.mail'

    def _get_unsubscribe_url(self, cr, uid, mail, email_to, msg=None, context=None):
        # _logger.debug("ONESTEiN _get_unsubscribe_url()")
        if mail.mailing_id.allow_unsubscribe:
            return super(MailMail, self)._get_unsubscribe_url(cr, uid, mail, email_to, msg, context)
        else:
            return ""


    