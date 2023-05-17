# -*- coding: utf-8 -*-


from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError as Warning, ValidationError
import time

class ek_contract_work_guide(models.Model):
    _inherit = 'ek.contract.work.guide'

    #
    # @api.model
    # def metodo_execution(self):
    #     records = self.env['ek.contract.work.guide'].sudo().search([('name', '=', self.name)])
    #     records.action_done_execution()


    def action_done_execution(self):
        guide = self.env['ek.contract.work.guide'].search([])
        for order in guide:
            all_executed = True
            for line in order.order_ids:
                if line.state != 'executed':
                    all_executed = False
                    break
            if all_executed:
                order.write({'state': 'executed', 'executed_date': time.strftime('%Y-%m-%d %H:%M:%S')})
