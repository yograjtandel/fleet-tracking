# -*- coding: utf-8 -*-
{
    'name': "fleet_tracking",
    'version' : '1.0',
    'depends' : ['base'],
    'author' : 'yog',
    'category' : 'Category',
    'description ' : """
    Description text
    """,

    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/vehicle_model_brand_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}