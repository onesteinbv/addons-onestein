# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.tools import ustr


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    period_start = fields.Many2one(
        'account.period',
        string='Start Period',
        required=True
    )
    period_stop = fields.Many2one(
        'account.period',
        string='Stop Period',
        required=True
    )
    date_from = fields.Date(
        related='period_start.date_start',
        string='Start Date',
        required=True,
        store=True
    )
    date_to = fields.Date(
        related='period_stop.date_stop',
        string='End Date',
        required=True,
        store=True
    )

    @api.multi
    @api.onchange('period_start')
    def _onchange_period_start(self):
        for line in self:
            if line.period_start:
                line.date_from = line.period_start.date_start

    @api.multi
    @api.onchange('period_stop')
    def _onchange_period_stop(self):
        for line in self:
            if line.period_stop:
                line.date_to = line.period_stop.date_stop

    def _prac_amt(self, cr, uid, ids, context=None):
        res = super(CrossoveredBudgetLines, self)._prac_amt(
            cr, uid, ids, context=context)
        if context is None:
            context = {}
        account_obj = self.pool.get('account.account')
        for line in self.browse(cr, uid, ids, context=context):
            result = 0.0
            acc_ids = [x.id for x in line.general_budget_id.account_ids]
            if not acc_ids:
                raise osv.except_osv(
                    _('Error!'),
                    _("The Budget '%s' has no accounts!") % ustr(
                        line.general_budget_id.name))
            acc_ids = account_obj._get_children_and_consol(
                cr, uid, acc_ids, context=context)
            date_from = line.period_start.date_start
            date_to = line.period_stop.date_stop
            if line.analytic_account_id.id:
                # lines without move_id.period_id: match on date
                cr.execute("""
                SELECT SUM(aal.amount)
                FROM account_analytic_line aal
                LEFT JOIN account_move_line aml
                    ON aml.id = aal.move_id
                WHERE aal.account_id=%s
                AND aal.date BETWEEN to_date(%s,'yyyy-mm-dd')
                    AND to_date(%s,'yyyy-mm-dd')
                AND aal.general_account_id=ANY(%s)
                AND aml.period_id is null
                """, (
                    line.analytic_account_id.id,
                    date_from,
                    date_to,
                    acc_ids
                ))
                result += cr.fetchone()[0] or 0.00

                # lines with move_id.period_id: match on period
                cr.execute("""
                SELECT SUM(aal.amount)
                FROM account_analytic_line aal
                INNER JOIN account_move_line aml
                    ON aml.id = aal.move_id
                INNER JOIN account_period ap
                    ON ap.id = aml.period_id
                WHERE aal.account_id=%s
                AND ap.id in (
                    SELECT id
                    from account_period
                    where date_start BETWEEN to_date(%s,'yyyy-mm-dd')
                        AND to_date(%s,'yyyy-mm-dd')
                )
                AND aal.general_account_id=ANY(%s)
                """, (
                    line.analytic_account_id.id,
                    date_from,
                    date_to,
                    acc_ids
                ))
                result += cr.fetchone()[0] or 0.00
            res[line.id] = result
        return res

    @api.model
    def create(self, vals):
        if vals.get('period_start') and vals.get('period_stop'):
            Period = self.env['account.period']
            period_start = Period.browse(vals.get('period_start'))
            period_stop = Period.browse(vals.get('period_stop'))
            warning = _('End period can never be earlier than start period!')
            if period_start != period_stop:
                if period_stop.date_start < period_start.date_start:
                    raise Warning(warning)
                if period_stop.date_stop < period_start.date_stop:
                    raise Warning(warning)
            if vals.get('period_start'):
                if period_start.date_start != vals.get('date_from'):
                    vals['date_from'] = period_start.date_start
            if vals.get('period_stop'):
                if period_stop.date_stop != vals.get('date_to'):
                    vals['date_to'] = period_stop.date_stop

        return super(CrossoveredBudgetLines, self).create(vals)

    @api.multi
    def write(self, vals):
        ctx = self._context
        if ctx and not ctx.get('skip_period_date_sync'):
            Period = self.env['account.period']
            if 'period_start' in vals:
                period_start = None
                if vals.get('period_start'):
                    period_start = Period.browse(vals.get('period_start'))
            if 'period_stop' in vals:
                period_stop = None
                if vals.get('period_stop'):
                    period_stop = Period.browse(vals.get('period_stop'))

            for budget in self:
                if 'period_start' not in vals:
                    period_start = budget.period_start
                if 'period_stop' not in vals:
                    period_stop = budget.period_stop

                if period_start and period_stop:
                    warning = _(
                        'End period can never be earlier than start period!'
                    )
                    if period_start != period_stop:
                        if period_stop.date_start < period_start.date_start:
                            raise Warning(warning)
                        if period_stop.date_stop < period_start.date_stop:
                            raise Warning(warning)
            if vals.get('period_start') and period_start:
                if period_start.date_start != vals.get('date_from'):
                    vals['date_from'] = period_start.date_start
            if vals.get('period_stop') and period_stop:
                if period_stop.date_stop != vals.get('date_to'):
                    vals['date_to'] = period_stop.date_stop

        return super(CrossoveredBudgetLines, self).write(vals)
