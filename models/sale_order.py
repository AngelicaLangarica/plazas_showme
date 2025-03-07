# -*- coding: utf-8 -*-
# Developed By Hector M. Chavez Cortez, Angelica Langarica Escobedo

from flectra import models, fields, api, _
from flectra.osv import expression

class SaleOrderPlazas(models.Model):
    _inherit = 'sale.order'

    plaza_id = fields.Many2one('plazas.manager', string="Plaza", tracking=True)

    @api.onchange('partner_id','partner_shipping_id')
    def _change_partner_plaza(self):
        for rec in self:
            if rec.partner_shipping_id:
                rec.plaza_id = rec.partner_shipping_id.plaza_id.id
            else:
                rec.plaza_id = False
    
    @api.onchange('partner_id')
    def _set_related_partners(self):
        shipping_partner = self.partner_id and self.env['res.partner'].sudo().search([('parent_id', '=', self.partner_id.id),('type', 'in', ['delivery'])])
        invoice_partner = self.partner_id and self.env['res.partner'].sudo().search([('parent_id', '=', self.partner_id.id),('type', 'in', ['invoice'])])
        shipping_domain = []
        invoice_domain = []
        res = {}
        if shipping_partner:
            shipping_domain = expression.AND([shipping_domain, [('id', 'in', shipping_partner.mapped('id'))]])
        if invoice_partner:
            invoice_domain = expression.AND([invoice_domain, [('id', 'in', invoice_partner.mapped('id'))]])

        res['domain'] = {'partner_shipping_id': shipping_domain, 'partner_invoice_id': invoice_domain}
        return res
    
    # FUNCTION INHERITED FROM flectra/addons/sale/models/sale.py
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment terms
        - Invoice address
        - Delivery address
        - Sales Team
        """
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'fiscal_position_id': False,
            })
            return

        self = self.with_company(self.company_id)

        # BLOCK ADDED BY LUCION
        invoice_partner = self.partner_id and self.env['res.partner'].sudo().search([('parent_id', '=', self.partner_id.id),('type', 'in', ['invoice'])])
        # END BLOCK LUCION

        # FUNCTION addres_get ORIGINAL FROM /flectra/flectra/addons/base/res_partner.py
        addr = self.partner_id.address_get(['delivery', 'invoice'])
        partner_user = self.partner_id.user_id or self.partner_id.commercial_partner_id.user_id
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': invoice_partner[0].id if invoice_partner else addr['invoice'], # LINE MODIFIED BY LUCION
            'partner_shipping_id': addr['delivery'],
        }
        user_id = partner_user.id
        if not self.env.context.get('not_self_saleperson'):
            user_id = user_id or self.env.context.get('default_user_id', self.env.uid)
        if user_id and self.user_id.id != user_id:
            values['user_id'] = user_id

        if self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms') and self.env.company.invoice_terms:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.company.invoice_terms
        if not self.env.context.get('not_self_saleperson') or not self.team_id:
            values['team_id'] = self.env['crm.team'].with_context(
                default_team_id=self.partner_id.team_id.id
            )._get_default_team_id(domain=['|', ('company_id', '=', self.company_id.id), ('company_id', '=', False)], user_id=user_id)
        self.update(values)