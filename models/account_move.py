# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'



    def cron_payment_concillation(self):
        invoices_ids = self.env['account.move'].search([('amount_residual', '<=', 0),
                                                        ('is_collector', '=', True),
                                                        ])
        for invoice in invoices_ids:
            invoice.write({'payment_state': 'paid'})



