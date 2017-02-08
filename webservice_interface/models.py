# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Onestein (<http://www.onestein.nl>).
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

from openerp import models, fields, api
from openerp.exceptions import Warning

import requests
from requests.auth import HTTPBasicAuth
import json


class WebService(models.Model):
    _name = 'web.service'

    name = fields.Char(string="Title", required=True)
    url = fields.Char(string="URL", required=True)
    username = fields.Char(string="Username", required=True)
    password = fields.Char(string="Password", required=True)

    type = fields.Selection([('http_rest', 'HTTP REST')], 'Service Type', required=True)

    description = fields.Text()

    def send(self, method, params=None, payload=None):
        if self.type == 'http_rest':
            headers = {'content-type': 'application/json'}

            response = requests.post(
                self.url + method,
                params=params,
                data=payload and json.dumps(payload) or None,
                headers=headers,
                verify=False,
                auth=HTTPBasicAuth(self.username, self.password))

            if response.status_code < 200 or response.status_code >= 300:
                raise Warning("ERROR " + str(response.status_code) + ": " + response.text)

            return response.json()
        else:
            raise Warning('Implementation for this web service type is missing: ' + self.type)

    def receive(self, method, params=None):
        if self.type == 'http_rest':
            headers = {'content-type': 'application/json'}
            
            response = requests.get(
                self.url + method, 
                params=params,
                headers=headers, 
                verify=False, 
                auth=HTTPBasicAuth(self.username, self.password))

            if response.status_code < 200 or response.status_code >= 300:
                raise Warning("ERROR " + str(response.status_code) + ": " + response.text)

            return response.json()
        else:
            raise Warning('Implementation for this web service type is missing: ' + self.type)
