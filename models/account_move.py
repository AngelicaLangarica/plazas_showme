# -*- coding: utf-8 -*-
# Developed By Hector M. Chavez Cortez, Angelica Langarica Escobedo

from flectra import models, fields, api, _
from flectra.osv import expression
import pytz
from datetime import datetime
import json
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
        user_tz = pytz.timezone(self.env.user.tz) if self.env.user.tz else pytz.timezone('America/Mexico_City')
        return pytz.utc.localize(datetime.today()).astimezone(user_tz).date() if user_tz else datetime.today().date()
    
    plaza_id = fields.Many2one('plazas.manager', string="Plaza", tracking=True, default=set_default_plaza)
    payment_history_id = fields.One2many('account.payment.history','move_id',string="Payment related")
    payment_date_save = fields.Date(string="Fecha de pago", store=True, compute="_compute_date", tracking=True)
    payment_date_registred = fields.Date(string="Fecha pagada", store=True, compute="_compute_date", tracking=True)
    total_no_credit = fields.Monetary(string='Total sin notas')
    total_no_credit_taxed = fields.Monetary(string='Total sin notas/Impuestos')

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
                rec.plaza_id = rec.partner_shipping_id.plaza_id
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
            dates = []
            load_json = json.loads(rec.invoice_payments_widget)
            if load_json:
                if rec.payment_state == 'paid':
                    if rec.invoice_payments_widget:
                        rec.payment_date_registred = self.today_date()
                        for item in load_json['content']:
                            dates.append(item['date'])
                            rec.create_history(item)
                        dates.sort()
                        if not rec.payment_date_save:
                            rec.payment_date_save = dates[-1]
                    elif not rec.payment_date_save:
                        rec.payment_date_save = False
                elif rec.payment_state == 'partial':
                    rec.payment_date_registred = False
                    for item in load_json['content']:
                        dates.append(item['date'])
                        rec.create_history(item)
                    dates.sort()
                else:
                    if not rec.payment_date_save:
                        rec.payment_date_save = False
                        rec.payment_date_registred = False
                # recorremos el contenido del json para identificar si el movimiento es una nota de credito, para eso sacamos el move_id
                # y buscamos en account.move por ese id y especificamente el campo move_type igualamos a out_refund, si esto es ok
                # se procede a realizar las operaciones necesarias, se aplica suma puesto que una nota de credito se registra en negativo
                # 1000 + (-800) = 200
                for note in load_json['content']:
                    if note['move_id']:
                        is_credit_note = self.env['account.move'].sudo().search([('id', '=', note['move_id']),('move_type', 'in', ['out_refund'])])
                        if is_credit_note:
                            total_taxed = rec.amount_total_signed + is_credit_note.amount_total_signed
                            total_untaxed = rec.amount_untaxed_signed + is_credit_note.amount_untaxed_signed
                            rec.total_no_credit = total_untaxed
                            rec.total_no_credit_taxed = total_taxed
                    else:
                        rec.total_no_credit = rec.amount_untaxed_signed
                        rec.total_no_credit_taxed = rec.amount_total_signed
            else:
                rec.payment_date_save = False
                rec.payment_date_registred = False

    def create_history(self, item):
        instance_history = self.env['account.payment.history'].sudo()
        payment_id = item['account_payment_id']
        data = {
            'move_id': self.id,
            'payment_id': payment_id,
        }
        exists_pay = instance_history.search([('move_id', '=', self.id),('payment_id', '=', payment_id)],limit=1)
        if not exists_pay:
            instance_history.create(data)