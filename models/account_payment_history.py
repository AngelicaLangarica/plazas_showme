# -*- coding: utf-8 -*-
# Developed By Hector M. Chavez Cortez, Angelica Langarica Escobedo

from flectra import models, fields, api, _
from datetime import datetime
import pytz
import logging

_logger = logging.getLogger(__name__)
class AccountPaymentRegister(models.Model):
    _name = 'account.payment.history'

    def today_date(self):
        user_tz = pytz.timezone(self.env.user.tz) if self.env.user.tz else pytz.timezone('America/Mexico_City')
        return pytz.utc.localize(datetime.today()).astimezone(user_tz).date() if user_tz else datetime.today().date()
    
    move_id = fields.Many2one('account.move', string="Factura relacionada")
    move_date = fields.Date(string="Fecha de registro", default=lambda self: self.today_date(), tracking=True)
    payment_date = fields.Date(string="Fecha del pago", related="payment_id.date")
    pay_date_saved = fields.Date(string="Fecha Marcada Pagada", related="move_id.payment_date_save")
    payment_id = fields.Many2one('account.payment', string="Pago Relacionado")
    amount = fields.Monetary(string="Monto", related="payment_id.amount")
    currency_id = fields.Many2one('res.currency', related='payment_id.currency_id')