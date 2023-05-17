import string

from odoo import models, fields , api,  _
# import datetime
# import time
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import UserError, ValidationError


class EkPromisePayment(models.Model):
    _inherit = 'ek.promise.payment'
    _rec_name = 'subscription_id'

    type_id=fields.Selection([('request', 'Solicitud de Cliente'), ('confirm', 'Confirmar Pago')],string="Tipo de Solicitud",required=True)

    year_repetition_count = fields.Integer(
        string='Conteo por ano',
        compute='_compute_year_repetition_count',
        store=True,
        readonly=True,
    )

    @api.depends('subscription_id', 'type_id')
    def _compute_year_repetition_count(self):
        for promise in self:
            domain = [
                ('subscription_id', '=', promise.subscription_id.id),
                ('type_id', '=', 'request'),
                ('create_date', '>=', datetime.now().strftime('%Y-01-01')),
            ]
            count = self.env['ek.promise.payment'].search_count(domain)
            promise.year_repetition_count = count

    @api.constrains('subscription_id', 'type_id')
    def _check_repetition_limit(self):
        for promise in self:
            if promise.type_id == 'request' and promise.year_repetition_count >= 4:
                raise UserError(_('No se pueden crear más promesas de pago para la misma suscripción.'))

    @api.onchange('subscription_id')
    def _onchange_subscription_id(self):
        for rec in self:
            rec.order_id = False
