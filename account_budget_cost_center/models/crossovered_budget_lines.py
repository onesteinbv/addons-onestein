# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, _
from openerp.models import NewId
from openerp.exceptions import Warning as UserError
from openerp.tools import ustr, DEFAULT_SERVER_DATE_FORMAT
import openerp.addons.decimal_precision as dp


class crossovered_budget_lines(models.Model):
    _inherit = "crossovered.budget.lines"

    @api.multi
    @api.depends('general_budget_id', 'general_budget_id.account_ids', 'date_to', 'date_from', 'analytic_account_id')
    def _get_practical_amount(self):
        account_obj = self.pool.get('account.account')
        for line in self:
            result = 0.0
            acc_ids = [x.id for x in line.general_budget_id.account_ids]
            if not acc_ids:
                raise UserError(_("Error! The Budget '%s' has no accounts!") % ustr(line.general_budget_id.name))
            acc_ids = account_obj._get_children_and_consol(self._cr, self._uid, acc_ids, context=self._context)
            date_to = line.date_to
            date_from = line.date_from
            crossovered_budget_id = line.crossovered_budget_id

            if crossovered_budget_id and isinstance(crossovered_budget_id.id, (NewId)):
                continue

            costcenter = crossovered_budget_id and crossovered_budget_id.cost_center_id or None
            if costcenter and date_from and date_to:
                self._cr.execute(
                    "SELECT SUM(debit) - SUM(credit) FROM account_move_line WHERE cost_center_budget_id=%s AND (date "
                    "between to_date(%s,'yyyy-mm-dd') AND to_date(%s,'yyyy-mm-dd')) AND "
                     "account_id=%s ",
                    (crossovered_budget_id.id, date_from, date_to, line.general_budget_id.account_id.id )
                )
                result = self._cr.fetchone()[0]
            elif line.analytic_account_id and date_from and date_to:
                self._cr.execute(
                    "SELECT SUM(amount) FROM account_analytic_line WHERE account_id=%s AND (date "
                    "between to_date(%s,'yyyy-mm-dd') AND to_date(%s,'yyyy-mm-dd')) AND "
                    "general_account_id=ANY(%s)", (line.analytic_account_id.id, date_from, date_to, acc_ids,)
                )
                result = self._cr.fetchone()[0]
            if result is None:
                result = 0.00
            line.practical_amount = result

    practical_amount = fields.Float(
        compute='_get_practical_amount',
        string='Practical Amount',
        digits_compute=dp.get_precision('Account')
    )

    @api.multi
    def unlink(self):
        for line in self:
            result = None
            crossovered_budget_id = line.crossovered_budget_id
            date_to = line.date_to
            date_from = line.date_from
            costcenter = crossovered_budget_id and crossovered_budget_id.cost_center_id or None
            if costcenter and date_from and date_to:
                self._cr.execute(
                    "SELECT id FROM account_move_line WHERE cost_center_budget_id=%s AND (date "
                    "between to_date(%s,'yyyy-mm-dd') AND to_date(%s,'yyyy-mm-dd')) AND "
                     "account_id=%s ",
                    (crossovered_budget_id.id, date_from, date_to, line.general_budget_id.account_id.id )
                )
                result = self._cr.fetchone()
            if result:
                warning_msg = _('Is not possible to delete the budget line because journal entries are posted on the account!')
                raise UserError(warning_msg)
            super(crossovered_budget_lines, line).unlink()
        return True
