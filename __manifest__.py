# -*- coding: utf-8 -*-
# Developed By Hector M. Chavez Cortez, Angelica Langarica Escobedo

{
    'name': 'Plazas Manager Showme',
    'summary': 'Plazas Manager Showme',
    'description': 'This module allow create plazas in showme',
    'author': 'Lucion',
    'website': 'https://lucion.mx',
    'category': 'Tools',
    'version': '1.0',
    'depends': ['base','sale_management','account','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/plazas_manager_view.xml',
        'views/sale_order_view.xml',
        'views/product_template_view.xml',
        'views/account_move_view.xml',
        'views/account_payment_view.xml',
    ],
    'application': True,
    'installable': True,
}