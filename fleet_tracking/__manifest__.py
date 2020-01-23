# -*- coding: utf-8 -*-
{
    'name': "fleet_tracking",
    'version' : '1.0',
    'depends' : ['base','website','web_dashboard'],
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
        'views/fleet_vehicle_view.xml',
        'views/fleet_vehicle_contract_view.xml',        
        'views/fleet_cost_view.xml',
        'views/fleet_odometer_view.xml',
        'views/fleet_odometer_templet.xml',
        'views/fleet_dashboard_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True
}