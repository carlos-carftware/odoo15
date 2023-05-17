# -*- coding: utf-8 -*-


from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError as Warning, ValidationError
import time


class ek_contract_work_order(models.Model):
    _inherit = 'ek.contract.work.order'

    subscription_id = fields.Many2one(comodel_name="sale.subscription", string="Contrato", required=False,
                                     )
    is_oamp = fields.Boolean(compute='_compute_is_oamp', store=True)

    is_olin = fields.Boolean(compute='_compute_is_olin', store=True)


    @api.depends('type_id.code')
    def _compute_is_oamp(self):
        for record in self:
            record.is_oamp = (record.type_id.code == 'OAMP')


    @api.depends('type_id.code')
    def _compute_is_olin(self):
        for record in self:
            record.is_olin = (record.type_id.code == 'OLIN')



    def open_new_service_cut_date_form(self):
        return {
            'name': 'Open Form Pack',
            'type': 'ir.actions.act_window',
            'res_model': 'ek.contract.cut.line',
            'res_id': self.new_service_cut_date.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    def open_package_id_form(self):
        return {
            'name': 'Open Form Pack',
            'type': 'ir.actions.act_window',
            'res_model': 'ek.isp.package',
            'res_id': self.package_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    def open_bandwidth_up_id_form(self):
        return {
            'name': 'Open Form banup',
            'type': 'ir.actions.act_window',
            'res_model': 'ek.bandwidth',
            'res_id': self.bandwidth_up_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    def open_bandwidth_down_id_form(self):
        return {
            'name': 'Open Form bandown',
            'type': 'ir.actions.act_window',
            'res_model': 'ek.bandwidth',
            'res_id': self.bandwidth_down_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    def open_core_id_form(self):
        return {
            'name': 'Open Form core',
            'type': 'ir.actions.act_window',
            'res_model': 'isp.core',
            'res_id': self.core_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    def open_ap_id_form(self):
        return {
            'name': 'Open Form apk',
            'type': 'ir.actions.act_window',
            'res_model': 'isp.ap',
            'res_id': self.ap_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    def open_box_id_form(self):
        return {
            'name': 'Open Form box',
            'type': 'ir.actions.act_window',
            'res_model': 'isp.box',
            'res_id': self.box_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    def open_olt_id_form(self):
        return {
            'name': 'Open Form olt',
            'type': 'ir.actions.act_window',
            'res_model': 'isp.olt',
            'res_id': self.olt_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    def open_card_id_form(self):
        return {
            'name': 'Open Form card',
            'type': 'ir.actions.act_window',
            'res_model': 'isp.olt.card',
            'res_id': self.card_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    def open_port_id_form(self):
        return {
            'name': 'Open Form Port',
            'type': 'ir.actions.act_window',
            'res_model': 'isp.olt.card.port',
            'res_id': self.port_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    def open_vlan_id_form(self):
        return {
            'name': 'Open Form vlan',
            'type': 'ir.actions.act_window',
            'res_model': 'ek.isp.vlan',
            'res_id': self.vlan_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    def open_ip_id_form(self):
        return {
            'name': 'Open Form IP',
            'type': 'ir.actions.act_window',
            'res_model': 'isp.ip.address',
            'res_id': self.ip_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }


class ek_isp_package(models.Model):
    _inherit =  'ek.isp.package'



