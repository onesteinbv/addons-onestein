# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api
from openerp.exceptions import Warning
from openerp.tools.translate import _


class HrAnalyticTimesheet(models.Model):
    _inherit = 'hr.analytic.timesheet'

    @api.model
    def create(self, vals):
        account_obj = self.env['account.analytic.account']
        account = account_obj.browse(vals['account_id'])
        if 'unit_amount' in vals and vals['unit_amount']:
            if account.alert_writing_hours == 'block' and account.limit_hours:
                total_hours = 0.0
                for line in account.line_ids:
                    total_hours += line.unit_amount
                if (account.limit_hours - total_hours - vals['unit_amount']) < 0.0:
                    raise Warning(
                        _("Maximum hours for this project has been reached,\n please contact the project manager %s")
                        % (account.manager_id and account.manager_id.name or ''))
        if 'date' in vals and vals['date']:
            if account.limit_date_start:
                if vals['date'] < account.limit_date_start:
                    raise Warning(
                        _("Selected Date cannot be less than the Start Date limit defined in the contract"))
            if account.limit_date_end:
                if vals['date'] > account.limit_date_end:
                    raise Warning(
                        _("Selected Date cannot be greater than the End Date limit defined in the contract"))

        return super(HrAnalyticTimesheet, self).create(vals)

    @api.multi
    def write(self, vals):
        orig_account = None
        if 'account_id' in vals and vals['account_id']:
            account_obj = self.env['account.analytic.account']
            orig_account = account_obj.browse(vals['account_id'])
        for timesheet in self:
            if not orig_account:
                account = timesheet.account_id
            else:
                account = orig_account
            if 'unit_amount' in vals and vals['unit_amount']:
                if account and account.alert_writing_hours == 'block' and account.limit_hours:
                    total_hours = 0.0
                    for line in account.line_ids:
                        if timesheet.line_id and line.id != timesheet.line_id.id:
                            total_hours += line.unit_amount
                    if (account.limit_hours - total_hours - vals['unit_amount']) < 0.0:
                        raise Warning(
                            _("Maximum hours for this project has been reached,\n please contact the project manager %s")
                            % (account.manager_id and account.manager_id.name or ''))
            if 'date' in vals and vals['date']:
                if account.limit_date_start:
                    if vals['date'] < account.limit_date_start:
                        raise Warning(
                            _("Selected Date cannot be less than the Start Date limit defined in the contract"))
                if account.limit_date_end:
                    if vals['date'] > account.limit_date_end:
                        raise Warning(
                            _("Selected Date cannot be greater than the End Date limit defined in the contract"))

        return super(HrAnalyticTimesheet, self).write(vals)

    @api.multi
    def check_expected_hours_reached(self, amount):
        for timesheet in self:
            account = timesheet.account_id
            if account.alert_writing_hours in ['alert', 'block'] and account.limit_hours:
                total_hours = 0.0
                limit = account.limit_hours
                alert_limit = account.limit_hours * (account.limit_percentage or 0.0) / 100
                for line in account.line_ids:
                    if line.id != timesheet.id:
                        total_hours += line.unit_amount
                if (limit - total_hours - amount) < 0.0:
                    account_manager_name = account.manager_id and \
                        account.manager_id.name or ''
                    raise Warning(
                        _("Maximum hours for this project has been reached,\n"
                          "please contact the project manager %s")
                        % account_manager_name)
                if alert_limit:
                    if (alert_limit - total_hours - amount) < 0.0:
                        account_manager_name = account.manager_id and \
                            account.manager_id.name or ''
                        raise Warning(
                            _("%s of hours for this project has been exceeded,\n"
                              "please contact the project manager %s")
                            % (account.limit_percentage, account_manager_name))

    @api.cr_uid_ids_context
    def on_change_unit_amount_account(self, cr, uid, ids, prod_id, unit_amount, company_id, unit=False, journal_id=False, account_id=False, context=None):
        if not context:
            context = {}
        account_obj = self.pool.get('account.analytic.account')
        timesheet_obj = self.pool.get('hr.analytic.timesheet')

        if ids:
            self.check_expected_hours_reached(cr, uid, ids, unit_amount, context)
        else:
            if account_id:
                amount = unit_amount or 0.0
                account = account_obj.browse(cr, uid, account_id, context)
                if account.alert_writing_hours in ['alert', 'block'] and account.limit_hours:
                    total_hours = 0.0
                    limit = account.limit_hours
                    alert_limit = account.limit_hours * (account.limit_percentage or 0.0) / 100
                    for line in account.line_ids:
                        total_hours += line.unit_amount

                    if (limit - total_hours - amount) < 0.0:
                        account_manager_name = account.manager_id and \
                            account.manager_id.name or ''
                        raise Warning(
                            _("Maximum hours for this project has been reached,\n"
                              "please contact the project manager %s")
                            % account_manager_name)
                    if alert_limit:
                        if (alert_limit - total_hours - amount) < 0.0:
                            account_manager_name = account.manager_id and \
                                account.manager_id.name or ''
                            raise Warning(
                                _("%s of hours for this project has been exceeded,\n"
                                  "please contact the project manager %s")
                                % (account.limit_percentage, account_manager_name))

        return timesheet_obj.on_change_unit_amount(cr, uid, ids, prod_id, unit_amount, company_id, unit, journal_id, context=context)
