# -*- coding: utf-8 -*-
# Copyright 2014 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
import openerp.addons.decimal_precision as dp


_logger = logging.getLogger(__name__)


class AccountInvoiceSpreadLine(models.Model):
    _name = 'account.invoice.spread.line'
    _description = 'Account Invoice Spread Lines'

    _order = 'line_date'

    name = fields.Char('Spread Name', size=64, readonly=True)
    invoice_line_id = fields.Many2one(
        comodel_name='account.invoice.line',
        string='Invoice Line',
        required=True)
    previous_id = fields.Many2one(
        comodel_name='account.invoice.spread.line',
        string='Previous Spread Line',
        readonly=True)
    amount = fields.Float(
        digits=dp.get_precision('Account'),
        required=True)
    remaining_value = fields.Float(
        string='Next Period Spread',
        digits=dp.get_precision('Account'))
    spreaded_value = fields.Float(
        string='Amount Already Spread',
        digits=dp.get_precision('Account'))
    line_date = fields.Date(
        string='Date',
        required=True)
    move_id = fields.Many2one(
        comodel_name='account.move',
        string='Spread Entry',
        readonly=True)
    move_check = fields.Boolean(
        compute='_compute_move_check',
        string='Posted',
        store=True)
    can_create_move = fields.Boolean(compute='_compute_can_create_move')
    sequence = fields.Integer(required=True, default=1)

    @api.multi
    def _check_invoice_number(self):
        """ Check invoice number """
        if not bool(filter(None, self.mapped(
            'invoice_line_id.invoice_id.internal_number'
        ))):
            raise ValidationError(
                _('Linked invoice has no internal number.'))

    @api.multi
    def _check_invoice_state(self):
        """ Check invoice state """
        self.ensure_one()
        state = self.mapped('invoice_line_id.invoice_id.state')[0]
        if state not in ('open', 'paid'):
            raise ValidationError(_('Cannot create moves when invoice state'
                                    ' is \'%s\'.') % (state,))

    @api.multi
    def _check_existing_move(self):
        """ Check existing move """
        self.ensure_one()
        if self.move_id:
            raise ValidationError(_('Move was already created.'))

    @api.multi
    def check_create_move(self):
        """ Check if a move can be created for this spread line """
        for this in self:
            this._check_existing_move()
            this._check_invoice_number()
            this._check_invoice_state()

    @api.depends(
        'move_id', 'invoice_line_id.invoice_id.state',
        'invoice_line_id.invoice_id.number'
    )
    def _compute_can_create_move(self):
        """ Computes 'can_create_move' """
        for this in self:
            this.can_create_move = True
            try:
                self.check_create_move()
            except ValidationError:
                this.can_create_move = False

    @api.depends('move_id')
    @api.multi
    def _compute_move_check(self):
        for this in self:
            this.move_check = bool(this.move_id)

    @api.model
    def _setup_move_data(self, spread_line, spread_date,
                         period_id):

        invoice = spread_line.invoice_line_id.invoice_id

        move_data = {
            'name': invoice.internal_number,
            'date': spread_date,
            'ref': spread_line.name,
            'period_id': period_id,
            'journal_id':
                spread_line.invoice_line_id.spread_journal_id.id or
                invoice.journal_id.id,
        }
        return move_data

    @api.model
    # pylint: disable=redefined-builtin
    def _setup_move_line_data(self, spread_line, spread_date,
                              period_id, account_id, type, move_id):
        invoice_line = spread_line.invoice_line_id

        if type == 'debit':
            debit = spread_line.amount
            credit = 0.0
        elif type == 'credit':
            debit = 0.0
            credit = spread_line.amount

        move_line_data = {
            'name': invoice_line.name,
            'ref': spread_line.name,
            'move_id': move_id,
            'account_id': account_id,
            'credit': credit,
            'debit': debit,
            'period_id': period_id,
            'journal_id': invoice_line.invoice_id.journal_id.id,
            'partner_id': invoice_line.invoice_id.partner_id.id,
            'date': spread_date,
            'analytic_account_id': invoice_line.account_analytic_id.id,
            }
        if 'cost_center_id' in invoice_line._fields:
            move_line_data['cost_center_id'] = invoice_line.cost_center_id.id
        return move_line_data

    @api.multi
    def create_move(self):
        """Used by a button to manually create a move from a spread line entry.
        Also called by a cron job."""
        period_obj = self.env['account.period']
        move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line']
        created_move_ids = []
        for line in self:
            invoice_line = line.invoice_line_id
            spread_date = line.line_date
            period_ids = period_obj.with_context(
                account_period_prefer_normal=True).find(spread_date)
            period_id = period_ids and period_ids[0] or False
            move_id = move_obj.create(
                self._setup_move_data(line, spread_date, period_id.id)
            )
            _logger.debug('MoveID: %s', (move_id.id,))

            if invoice_line.invoice_id.type in ('in_invoice', 'out_refund'):
                debit_acc_id = invoice_line.account_id.id
                credit_acc_id = invoice_line.spread_account_id.id
            else:
                debit_acc_id = invoice_line.spread_account_id.id
                credit_acc_id = invoice_line.account_id.id

            if invoice_line.invoice_id.move_id and\
                    invoice_line.spread_account_id:
                # we need to pretend to have the original invoice line
                # without spread, otherwise we won't find the line with
                # the original account
                data = invoice_line._convert_to_write({
                    key: value
                    for key, value in invoice_line._cache.items()
                    if key != 'spread_account_id'
                })
                # this might be empty, in this case, we do a noop write
                move_line = invoice_line.new(data)._find_move_line()
                move_line.write({
                    'account_id': invoice_line.spread_account_id.id,
                }, update_check=False)

            debit_move_line = move_line_obj.create(
                self._setup_move_line_data(
                    line, spread_date, period_id.id, debit_acc_id,
                    'debit', move_id.id
                )
            )
            credit_move_line = move_line_obj.create(
                self._setup_move_line_data(
                    line, spread_date, period_id.id, credit_acc_id,
                    'credit', move_id.id
                )
            )

            # Add move_id to spread line
            line.write({'move_id': move_id.id})

            # reconcile if possible
            if invoice_line.spread_account_id.reconcile:
                reconcile_move_line = invoice_line.invoice_id.type in (
                    'in_invoice', 'out_refund'
                ) and debit_move_line or credit_move_line
                (
                    reconcile_move_line +
                    invoice_line._find_move_line()
                ).reconcile_partial()
            created_move_ids.append(move_id.id)
        return created_move_ids

    @api.multi
    def open_move(self):
        """Used by a button to manually view a move from a
        spread line entry."""
        for line in self:
            return {
                'name': _("Journal Entry"),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'domain': [('id', '=', line.move_id.id)],
                }

    @api.multi
    # pylint: disable=no-value-for-parameter,arguments-differ
    def unlink(self):
        """ Unlink moves when unlinking spread lines """
        self.unlink_move()
        return super(AccountInvoiceSpreadLine, self).unlink()

    @api.multi
    def unlink_move(self):
        """Used by a button to manually unlink a move
        from a spread line entry."""
        for line in self:
            move = line.move_id
            if move.state == 'posted':
                move.button_cancel()
            move.unlink()
            line.move_id = False
        return True

    @api.multi
    def _create_entries(self):
        """Find spread line entries where date is in the past and
        create moves for them."""
        period_obj = self.env['account.period']
        periods = period_obj.with_context(
            account_period_prefer_normal=True).find(fields.Date.today())
        period = periods and periods[0] or False
        lines = self.search([
            ('line_date', '<=', period.date_stop),
            ('invoice_line_id.spread_account_id', '!=', False),
            ('invoice_line_id.invoice_id.state', '!=', 'cancel'),
            ('invoice_line_id.invoice_id.period_id.state', '!=', 'done'),
            ('move_id', '=', False),
        ])

        result = []
        for line in lines:
            result += line.create_move()
        return result
