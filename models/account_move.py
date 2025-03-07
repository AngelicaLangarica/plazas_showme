# -*- coding: utf-8 -*-
# Developed By Hector M. Chavez Cortez, Angelica Langarica Escobedo

from flectra import models, fields, api, _
from flectra.osv import expression
import logging

_logger = logging.getLogger(__name__)
class AccountMovePlazas(models.Model):
    _inherit = 'account.move'

    def set_default_plaza(self):
        _logger.info(f"Its Working {self.partner_shipping_id}")
        if self.partner_id:
            return self.partner_shipping_id.plaza_id    
        return self.partner_shipping_id.plaza_id

    plaza_id = fields.Many2one('plazas.manager', string="Plaza", tracking=True, default=set_default_plaza)

    @api.constrains('partner_id', 'partner_shipping_id')
    def _onchange_partner(self):
        for rec in self:
            _logger.info(f"Shipping Partner {rec.partner_id}----------{rec.partner_shipping_id.name}-----{rec.partner_id.name}-----{rec.plaza_id.name}")
            if rec.partner_shipping_id:
                rec.plaza_id = rec.partner_shipping_id.plaza_id
            else:
                _logger.info(f"otros------->")
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
