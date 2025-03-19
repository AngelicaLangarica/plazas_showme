# -*- coding: utf-8 -*-
# Developed By Hector M. Chavez Cortez, Angelica Langarica Escobedo

from flectra import models, fields, api, _
from flectra.osv import expression
import pytz
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)
class AccountMovePlazas(models.Model):
    _inherit = 'account.move'

    def set_default_plaza(self):
        _logger.info(f"Its Working {self.partner_shipping_id}")
        if self.id: 
            sales = self.env['sale.order'].sudo().search([('invoice_ids', 'in', self.ids)])
            if sales:
                plaza_id = sales[0].plaza_id
            return plaza_id
        elif self.partner_id:
            return self.partner_shipping_id.plaza_id    
        return self.partner_id.plaza_id

    def today_date(self):
        user_tz = pytz.timezone(self.env.user.tz)
        return pytz.utc.localize(datetime.today()).astimezone(user_tz).date() if user_tz else datetime.today().date()
    
    plaza_id = fields.Many2one('plazas.manager', string="Plaza", tracking=True, default=set_default_plaza)
    payment_history_id = fields.One2many('account.payment.history','move_id',string="Payment related")
    payment_date_save = fields.Date(string="Fecha de pago", store=True, compute="_compute_date", tracking=True)

    @api.constrains('partner_id', 'partner_shipping_id')
    def _constrains_partner(self):
        for rec in self:
            # Buscamos las ventas las cuales tengan ligada la factura en la que estamos
            sales = self.env['sale.order'].sudo().search([('invoice_ids', 'in', self.ids)])
            if sales:
                # solo tomamos la primera venta para evitar errores
                plaza_id = sales[0].plaza_id
            elif rec.partner_shipping_id:
                plaza_id = rec.partner_shipping_id.plaza_id
            else:
                plaza_id = False
            rec.plaza_id = plaza_id

    @api.onchange('partner_id','partner_shipping_id')
    def _onchange_partner_oninvoice(self):
        for rec in self:
            if rec.partner_shipping_id:
                rec.plaza_id = rec.partner_shipping_iVd.plaza_id
            else:
                rec.plaza_id = False

    @api.onchange('partner_id')
    def _set_related_partners(self):
        shipping_partner = self.plaza_id and self.env['res.partner'].sudo().search([('plaza_id', '=', self.plaza_id.id),('type', 'in', ['delivery'])])
        shipping_domain = []
        res = {}
        if shipping_partner:
            shipping_domain = expression.AND([shipping_domain, [('id', 'in', shipping_partner.mapped('id'))]])

        res['domain'] = {'partner_shipping_id': shipping_domain}
        return res

    @api.depends('payment_state')
    def _compute_date(self):
        for rec in self:
            if rec.payment_state == 'paid':
                rec.payment_date_save = rec.today_date()
            else:
                rec.payment_date_save = False