# -*- coding: utf-8 -*-
{
    'name': "modulos isp",

    'summary': """ """,

    'description': """

    """,

    'author': "CG",
    'website': "",

    'category': 'Uncategorized',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'sale_advance_payment', 'ek_sales_subscription', 'ek_isp_subscription',
                'ek_base_sales_subscription',
                'sale_subscription', 'base', 'account'],

    # always loaded
    'data': [
        'views/sale_order_view.xml',
        'views/ek_contract_work_order_view.xml',
        'views/ek_promise_payment_view.xml',
        'views/sale_subscription_view.xml',
        'data/cron_button_pay.xml',
        'data/cron_concilla_account.xml',
        'data/cron_cortes.xml',
        'data/cron_primero.xml',
        'data/cron_recurring.xml',
        'data/cron_state_executed.xml',

    ],


}
