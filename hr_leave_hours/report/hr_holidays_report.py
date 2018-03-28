# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import fields,osv

class hr_holidays_remaining_leaves_user(osv.osv):
    _inherit = "hr.holidays.remaining.leaves.user"
    _columns = {
        'no_of_hours': fields.float('Approved hours'),
        'virtual_hours': fields.float('Virtual hours'),
        'no_of_leaves': fields.integer('Remaining hours'),
        'employee_id': fields.many2one('hr.employee', 'Employee'),
        }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'hr_holidays_remaining_leaves_user')
        cr.execute("""
            CREATE or REPLACE view hr_holidays_remaining_leaves_user as (
                 SELECT
                    min(hrs.id) as id,
                    rr.name as name,
                    sum(hrs.number_of_hours) as no_of_leaves,
                    sum(case when type='remove' and extract(year from date_from) = extract(year from current_date) then hrs.number_of_hours else 0 end) as no_of_hours,
                    sum(case when (type='remove' and extract(year from date_from) = extract(year from current_date)) or (type='add' and extract(year from approval_date) = extract(year from current_date)) then hrs.virtual_hours else 0 end) as virtual_hours,
                    rr.user_id as user_id,
                    hhs.name as leave_type,
                    hre.id as employee_id
                FROM
                    hr_holidays as hrs, hr_employee as hre,
                    resource_resource as rr,hr_holidays_status as hhs
                WHERE
                    hrs.employee_id = hre.id and
                    hre.resource_id =  rr.id and
                    hhs.id = hrs.holiday_status_id
                GROUP BY
                    rr.name, rr.user_id, hhs.name, hre.id
            )
        """)

class hr_employee(osv.osv):
    _inherit = "hr.employee"
    _columns = {
        'remaining_hours_ids': fields.one2many('hr.holidays.remaining.leaves.user', 'employee_id', string='Remaining hours per Leave Type')
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
