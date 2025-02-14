# -*- coding: utf-8 -*-
# - Developed By Hector M. Chavez Cortez, Angelica Langarica Escobedo, Kevin Basilio Moreno

from flectra import models, fields, api, _

class ReportSale(models.Model):
    _inherit = 'sale.report'

    plaza_id = fields.Many2one('plazas.manager', string="Plazas")

    def _select_additional_fields(self, fields):
        """Hook to return additional fields SQL specification for select part of the table query.

        :param dict fields: additional fields info provided by _query overrides (old API), prefer overriding
            _select_additional_fields instead.
        :returns: mapping field -> SQL computation of the field
        :rtype: dict
        """
        fields['plaza_id'] = ', s.plaza_id AS plaza_id'
        return fields
