# Copyright 2017-2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, date
from odoo.tests import common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class TestHolidaysExpiration(common.TransactionCase):
    def setUp(self):
        super(TestHolidaysExpiration, self).setUp()

        self.Holidays = self.env['hr.holidays']
        self.HolidaysStatus = self.env['hr.holidays.status']
        self.Employee = self.env['hr.employee']
        self.Template = self.env['mail.template']

        self.today_start = datetime.today().replace(
            hour=8, minute=0, second=0)
        self.today_end = datetime.today().replace(
            hour=18, minute=0, second=0)

        today_start = self.today_start.strftime(DTF)
        today_end = self.today_end.strftime(DTF)

        self.template = self.Template.create({
            'name': 'Template 1',
            'email_from': 'info@openerp.com',
            'subject': 'Template Test',
            'email_to': '',
            'model_id': self.env.ref(
                'hr_holidays.model_hr_holidays').id,
        })

        self.employee_1 = self.Employee.create({
            'name': 'Employee 1',
        })

        self.status_1 = self.HolidaysStatus.create({
            'name': 'Repeating Status',
            'limit': True,
        })

        self.leave_1 = self.Holidays.create({
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
        self.Holidays.check_expiring()
