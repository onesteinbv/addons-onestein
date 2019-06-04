# Copyright 2019 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.http import route, Controller, request
from werkzeug.utils import redirect


class MainController(Controller):
    @route('/office-365-oauth/success', type='http')
    def success(self, **kwargs):
        user = request.env.user
        token = user.office_365_get_token(request.httprequest.url)
        user.office_365_persist_token(token)

        return redirect('/')
