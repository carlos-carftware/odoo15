from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
import pytz


class SaleOrder(models.Model):
    _inherit = "sale.order"


    promise_payment_line_ids = fields.One2many(comodel_name="ek.promise.payment",
                                               inverse_name="order_id", string="Promesa de Pago")
    type_subscription = fields.Selection(
        [("prepaid", "Pre-Pago"), ("postpaid", "Post-Pago")],
        string="Tipo de Suscripción",

    )
    sale_pedido = fields.Boolean(string="sale_pedido", compute="action_done1")
    subscription_updated = fields.Boolean(string='Suscripción actualizada')

    @api.onchange('ek_subscription_id')
    def _onchange_ek_subscription_id(self):
        for rec in self:
            expiration_date = False
            if rec.ek_subscription_id and rec.ek_subscription_id.service_cut_date and rec.ek_subscription_id.service_cut_date.day_execution > 0:
                now = datetime.now(pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC'))
                expiration_date = datetime.strptime(str(now.year) + '-' + str(now.month) + '-' + str(rec.ek_subscription_id.service_cut_date.day_execution), '%Y-%m-%d')
            rec.validity_date = expiration_date

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for rec in self:
            rec.validity_date = False


    def _prepare_subscription_data(self, template):
        values = super(SaleOrder, self)._prepare_subscription_data(template)
        values.update({
            'type_subscription': self.type_subscription,
        })
        return values

    def action_button_pay(self):
        for company in self.env['res.company'].search([]):
            subscriptions = self.env['sale.subscription'].with_context(company_id=company.id).with_company(
                company).search([('company_id', '=', company.id)])
            for subscription in subscriptions:
                sale_orders = subscription.order_line_ids.mapped('order_id')
                for order in sale_orders:
                    collectors = order.account_payment_ids.filtered(lambda p: p.is_collector and order.state == 'draft')
                    if collectors:
                        order.write({'state': 'done'})
                        #order.action_confirm()
                        payment_obj = self.env["sale.advance.payment.inv"].with_context(active_id=order.id,
                                                                                        active_ids=order.ids)
                        pay_id = payment_obj.create({'advance_payment_method': 'delivered'})
                        pay_id.create_invoices()
                        for ln in order:
                            invoice = ln.invoice_ids[0]
                            invoice.with_company(invoice.company_id).action_post()



    def update_subscription(self):
        if not self.ek_subscription_id or not self.order_line:
            raise UserError('No se puede actualizar, está vacía La Suscripción o Linea del pedido.')
        if self.subscription_updated:
            raise UserError('La suscripción ya ha sido actualizada anteriormente.')

        # now = datetime.now(pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC'))
        # expiration_date = datetime.strptime(str(now.year) + '-' + str(now.month) + '-' + str(self.ek_subscription_id.service_cut_date.day_execution), '%Y-%m-%d')
        # self.validity_date = expiration_date
        super().update_subscription()
        self.subscription_updated = True


