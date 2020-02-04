# -*- coding: utf-8 -*-
{
    'name': "fleet_tracking",
    'version' : '1.0',
    'depends' : ['base','web_dashboard','portal'],
    'author' : 'yog',
    'category' : 'Category',
    'description ' : """
    Description text
    """,

    'data': [
        'security/fleet_security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',

        'wizard/cancelled_reason.xml',

        
        'reports/reports.xml',
        'views/vehicle_brand_view.xml',
        'views/fleet_vehicle_view.xml',
        'views/fleet_vehicle_contract_view.xml',        
        'views/fleet_cost_view.xml',
        'views/fleet_odometer_view.xml',
        'views/fleet_odometer_templet.xml',
        'views/fleet_dashboard_view.xml',
        'views/registration.xml',
        'views/homepage_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True
}