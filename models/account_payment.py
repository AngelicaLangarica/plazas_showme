# -*- coding: utf-8 -*-
# Developed By Hector M. Chavez Cortez, Angelica Langarica Escobedo

from flectra import models, fields, api, _
from flectra.osv import expression
import logging

_logger = logging.getLogger(__name__)
class AccountPaymentPlazas(models.Model):
    _inherit = 'account.payment'

    def action_post(self):
        res = super().action_post()
        active_ids = self.env.context.get('active_ids')
        invoices_to_post = self.env['account.move'].sudo().search([('id', 'in', active_ids)])
        if invoices_to_post:
            for rec in invoices_to_post:
                self.env['account.payment.history'].sudo().create({'move_id': rec.id, 'move_date': rec.today_date(), 'payment_id': self.id})
        _logger.info(f"RES R {res}-----------> context R {self.env.context}------->payment created")
        return res