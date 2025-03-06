# -*- coding: utf-8 -*-
# Developed By Hector M. Chavez Cortez, Angelica Langarica Escobedo

from flectra import models, fields, api, _

class ResPartnerPlazas(models.Model):
    _inherit = 'res.partner'

    plaza_id = fields.Many2one('plazas.manager', string="Plaza", tracking=True)