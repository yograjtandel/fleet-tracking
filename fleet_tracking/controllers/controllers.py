# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import ValidationError
class FleetTracking(http.Controller):
    @http.route([
    	'/fleet_tracking/',
    	'/edit/<model("fleet.driver"):d>',
    	], auth='public', website=True)
    def index(self,d=None, **kw):
    	driver = http.request.env['fleet.driver']
    	return http.request.render('fleet_tracking.index', {'driver' : driver.search([]),
    														'd' : d})


    @http.route(['/delete/<model("fleet.driver"):d>',], auth='public', website=True)
    def delete(self,d):
    	d.unlink()
    	return http.request.redirect('/fleet_tracking/')


    @http.route(['/update/',
    		'/save/'], auth='public', website=True)
    def create_update(self,**kw):
    	driver = http.request.env['fleet.driver']
    	if kw['id']:
    		driver.search([]).browse([kw['id']]).write(kw)
    	else:
    		driver.create(kw)
    	return http.request.redirect('/fleet_tracking/')

    @http.route(['/create/',], auth='public', website=True)
    def create_form(self,**kw):
    	driver = http.request.env['fleet.driver']
    	return http.request.render('fleet_tracking.index', {'driver' : driver.search([]),
    														'create' : True})

