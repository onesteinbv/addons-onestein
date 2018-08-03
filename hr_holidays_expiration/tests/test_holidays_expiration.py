# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, date
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class TestHolidaysExpiration(common.TransactionCase):
    def setUp(self):
        super(TestHolidaysExpiration, self).setUp()

        self.today_start = datetime.today().replace(
            hour=8, minute=0, second=0)
        self.today_end = datetime.today().replace(
            hour=18, minute=0, second=0)

        today_start = self.today_start.strftime(DTF)
        today_end = self.today_end.strftime(DTF)

        self.template = self.env['mail.template'].create({
            'name': 'Template 1',
            'email_from': 'info@openerp.com',
            'subject': 'Template Test',
            'email_to': '',
            'model_id': self.env.ref(
                'hr_holidays.model_hr_holidays').id,
        })

        self.employee_1 = self.env['hr.employee'].create({
            'name': 'Employee 1',
        })

        self.status_1 = self.env['hr.holidays.status'].create({
            'name': 'Repeating Status',
            'limit': True,
        })

        self.leave_1 = self.env['hr.holidays'].create({
            'holiday_status_id': self.status_1.id,
            'holiday_type': 'employee',
            'type': 'add',
            'date_from': today_start,
            'date_to': today_end,
            'employee_id': self.employee_1.id,
            'expiration_date': date.today().strftime(DF),
            'email_notify': True,
            'notify_template_id': self.template.id,
            'expire_template_id': self.template.id,
        })

    def test_01_check_expiring(self):
        self.leave_1.action_approve()
        self.env['hr.holidays'].check_expiring()
