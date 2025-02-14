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
    'depends': ['sale','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/plazas_manager_view.xml',
        'views/sale_order_view.xml',
        'views/product_template_view.xml',
    ],
    'application': True,
    'installable': True,
}