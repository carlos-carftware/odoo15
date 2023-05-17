# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz


class ek_subscription_disabled(models.Model):
    _inherit = "ek.subscription.disabled"

    def cron_execute_cutting_off_process(self, custom_date=False):
        for company in self.env['res.company'].search([]):
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            custom_date = fields.Date.from_string(custom_date) if custom_date else datetime.now(tz=user_tz).date()
            disabled = self.env['ek.subscription.disabled'].with_context(company_id=company.id).with_company(
                company).search([
                ('state', 'in', ['draft', 'process']),
                ('date_cut', '=', custom_date)
                ,('company_id', '=', company.id)
            ])
            if disabled:
                for line in disabled.ek_disabled_ids:
                    # if line.date_cut == custom_date:
                    if line.subscription_id._get_amount_due(date_to=custom_date) <= 0:
                        continue
                    line.subscription_id.state_service = 'pending'
                    line.is_process_disabled = True
                    line.state_service = 'pending'
                    disabled.state = 'process'
                if all(line.subscription_id.state_service == 'pending' for line in disabled.ek_disabled_ids):
                    disabled.state = 'done'
