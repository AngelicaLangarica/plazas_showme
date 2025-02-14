# -*- coding: utf-8 -*-
# Developed By Hector M. Chavez Cortez, Angelica Langarica Escobedo

from flectra import models, fields, api, _

class PlazasManagerShowme(models.Model):
    _name = 'plazas.manager'
    _description = 'Set plazas in Showme'

    name = fields.Char(string="Nombre de la plaza", required=True)
    active = fields.Boolean(string="¿Activo?", default=True)


