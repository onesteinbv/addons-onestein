# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.exceptions import UserError, ValidationError


class TestPartnerSequence(common.TransactionCase):

    def setUp(self):
        super(TestPartnerSequence, self).setUp()
        self.Sequence = self.env['ir.sequence']
        self.Partner = self.env['res.partner']
        self.PartnerSequence = self.env['res.partner.sequence']

        self.sequence_1 = self.Sequence.create({
            'name': 'Test Sequence',
            'prefix': 'TEST',
        })

        self.partner_sequence_1 = self.PartnerSequence.create({
            'country_id': self.env.ref('base.it').id,
            'sequence_id': self.sequence_1.id,
        })

        self.partner_1 = self.Partner.create({
            'name': 'Test1',
            'is_company': True,
            'country_id': self.env.ref('base.it').id
        })

        self.partner_2 = self.Partner.create({
            'name': 'Test2',
            'is_company': True,
            'country_id': self.env.ref('base.be').id
        })

    def test_01_error(self):
        with self.assertRaises(ValidationError):
            self.Partner.create({
                'name': 'Test Fail',
                'is_company': True,
                'country_id': self.env.ref('base.it').id,
                'ref': self.partner_1.ref,
            })
        self.env.ref('partner_sequence.seq_res_partner').unlink()
        with self.assertRaises(UserError):
            self.Partner.create({
                'name': 'Test3',
                'is_company': True,
                'country_id': self.env.ref('base.be').id
            })
