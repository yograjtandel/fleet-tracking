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
        'reports/reports.xml',
        'views/vehicle_brand_view.xml',
        'views/fleet_vehicle_trip_view.xml',
        'views/fleet_vehicle_view.xml',
        'views/fleet_cost_view.xml',
        'views/fleet_odometer_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}