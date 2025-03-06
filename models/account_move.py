# -*- coding: utf-8 -*-
# Developed By Hector M. Chavez Cortez, Angelica Langarica Escobedo

from flectra import models, fields, api, _
from flectra.osv import expression

class AccountMovePlazas(models.Model):
    _inherit = 'account.move'

    plaza_id = fields.Many2one('plazas.manager', string="Plaza", tracking=True)

    # @api.onchange('partner_id','partner_shipping_id')
    # def _change_partner_plaza(self):
    #     if self.partner_id:
    #         self.plaza_id = self.partner_shipping_id.plaza_id.id
        

    # @api.onchange('partner_id')
    # def _set_related_partners(self):
    #     shipping_partner = self.plaza_id and self.env['res.partner'].sudo().search([('parent_id', '=', self.plaza_id.id),('type', 'in', ['delivery'])])
    #     shipping_domain = []
    #     res = {}
    #     if shipping_partner:
    #         shipping_domain = expression.AND([shipping_domain, [('id', 'in', shipping_partner.mapped('id'))]])

    #     res['domain'] = {'partner_shipping_id': shipping_domain}
    #     return res
