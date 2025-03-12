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
        user_tz = pytz.timezone(self.env.user.tz)
        return pytz.utc.localize(datetime.today()).astimezone(user_tz).date() if user_tz else datetime.today().date()
    
    move_id = fields.Many2one('account.move', string="Factura relacionada")
    move_date = fields.Date(string="Fecha de pago", default=lambda self: self.today_date(), tracking=True)
    #payment_import = fields.Monetary(string="Importe")
    #payment_status = fields.Char(string="Estado")

    # def _compute_import(self):
    #     for line in self:
    #         if line.move_id:
    #            line.payment_import = line.move_id.payment_state.amount
    #         else:
    #             line.payment_import = 0.0
        
