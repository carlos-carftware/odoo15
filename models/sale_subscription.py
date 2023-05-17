from num2words import num2words
import logging
from odoo import api, fields, models, _
import datetime
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from more_itertools import chunked


class sale_subscription(models.Model):
    _inherit = 'sale.subscription'

    type_subscription = fields.Selection(
        [("prepaid", "Pre-Pago"), ("postpaid", "Post-Pago")],
        string="Tipo de Suscripción",

    )

    def cron_recurring(self, date=False, subscription_id=False ,batch_size=20):
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
        today = fields.Date.from_string(date) if date else datetime.now(tz=user_tz).date()
        subscriptions = self.browse(subscription_id) if subscription_id else self.env['sale.subscription'].search([
            ('state_service', 'in', ['open', 'pending']),
            ('recurring_next_date', '!=', False),
        ])
        subscriptions_count = len(subscriptions)
        pages = (subscriptions_count // batch_size) + (subscriptions_count % batch_size and 1)
        for page in range(1, pages + 1):
            subscription_ids = subscriptions[((page - 1) * batch_size): (page * batch_size)].ids
            subscriptions_batch = self.env['sale.subscription'].browse(subscription_ids)
            for subscription in subscriptions_batch:
                recurring_next_date = subscription.recurring_next_date
                if recurring_next_date.month == today.month:
                    print(f"Ejecucion {subscription.id}")
                    subscription._recurring_create_sale()
                    subscription._cr.commit()

    def cron_generate_cutting_off_process(self, date=False):
        for company in self.env['res.company'].search([]):
            #subs = self.with_company(company_id).with_context(company_id=company_id).browse(sub_ids)
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            date = fields.Date.from_string(date) if date else datetime.now(tz=user_tz).date()
            subscriptions = self.env['sale.subscription'].with_context(company_id=company.id).with_company(
                company).search([('state_service', '=', 'open'), ('company_id', '=', company.id)])
            srch_cut_range = self.env['ek.contract.range.cut.line'].with_context(company_id=company).with_company(company).search([('day_execution', '=', date.day)])
            if srch_cut_range:
                subscription_ids = subscriptions.filtered(lambda s: s._get_amount_due(date_to=date) > 0)
            else:
                subscription_ids = subscriptions.filtered(lambda s: s._get_amount_due(date_to=date) > 0 and (not s.service_cut_date.day_execution or s.service_cut_date.day_execution != date.day))
            if subscription_ids:
                #now_date = datetime.now(tz=user_tz).date()
                holidays = [x.date for x in subscription_ids.service_cut_date.contract_range_id.holiday_cut_id.holiday_ids]
                # Dias ignorados
                days = [day.code for day in subscription_ids.service_cut_date.contract_range_id.day_cut_ids]
                final_day = []
                for day in days:
                    val = day - 1
                    if val == 0:
                        val = 7
                    final_day.append(val)
                # condition = False
                while True:
                    if (date.weekday() + 1) not in final_day and date not in holidays:
                        # condition = True
                        break
                    else:
                        date = date + timedelta(days=1)

                subscription_count = len(subscription_ids)
                total_amount = sum(subscription._get_amount_due(date_to=date) for subscription in subscription_ids)

                # Generar cabecera del proceso de corte
                disabled = self.env['ek.subscription.disabled'].sudo().create({
                    'service_cut_date': subscription_ids[0].service_cut_date.id,
                    'company_id': subscription_ids[0].company_id.id,
                    'name': self.env['ir.sequence'].next_by_code('ek.subscription.disabled') or '/',
                    'date_cut': date,
                    'count_disabled': subscription_count,
                    'state': 'draft',
                    'amount_disabled': total_amount,
                })
                # Crear y agregar líneas de contratos a cortar
                disabled_lines = []
                for subscription in subscription_ids:
                    line = self.env['ek.disabled.line'].create({
                        'subscription_id': subscription.id,
                        'subs_dis_id': disabled.id,
                        'date_cut': date,
                        'state_service': subscription.state_service,
                        'amount_due': subscription._get_amount_due(date_to=date),
                    })
                    disabled_lines.append(line)
                disabled.write({'ek_disabled_ids': [(6, 0, [line.id for line in disabled_lines])]})






