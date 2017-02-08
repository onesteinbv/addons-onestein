# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Onestein (<http://www.onestein.nl>).
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

import json
import datetime

from openerp.addons.web import http
from openerp.addons.web.http import request

class WebsiteCalendarBlock(http.Controller):
    
    #TODO: Is <datetime:start> implemented by Odoo?
    @http.route(['/calendar_block/get_events/<int:start>/<int:end>'], type='http', auth='public', website=True)
    def get_events(self, start, end, **post):
        cr, uid, context = request.cr, request.uid, request.context

        #Get events
        calendar_event_obj = request.registry['calendar.event']
        calendar_event_ids = calendar_event_obj.search(cr, uid, [('start', '<', unicode(datetime.datetime.fromtimestamp(end))), ('stop', '>', unicode(datetime.datetime.fromtimestamp(start)))], context=context)
        calendar_events = calendar_event_obj.browse(cr, uid, calendar_event_ids, context = context)
        
        contacts = []
        if request.website.user_id.id != uid:
            calendar_contact_obj = request.registry['calendar.contacts']
            calendar_contact_ids = calendar_contact_obj.search(cr, uid, [('user_id', '=', uid)], context=context)
            calendar_contacts = calendar_contact_obj.browse(cr, uid, calendar_contact_ids, context = context)
            
            #Create response (Cannot serialize object)
            contacts.append(request.env.user.partner_id.id)
            for contact in calendar_contacts:
                contacts.append(contact.partner_id.id)
        
        #Events
        events = []
        for calendar_event in calendar_events:
            #Fetch attendees
            attandees = []
            for attandee_id in calendar_event.attendee_ids:
                attandees.append({ 'id': attandee_id.partner_id.id, 'name': attandee_id.partner_id.name })

            events.append({
                           'id': calendar_event.id,
                           'start': calendar_event.start, 
                           'end': calendar_event.stop, 
                           'title': calendar_event.name,
                           'allDay': calendar_event.allday,
                           'color': calendar_event.color_partner_id,
                           'attendees': attandees
                           })
        
        return json.dumps({ 'events': events, 'contacts': contacts })
