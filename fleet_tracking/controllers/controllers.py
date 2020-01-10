# -*- coding: utf-8 -*-
from odoo import http

class Academy(http.Controller):
    @http.route([
    	'/fleet_tracking/',
    	'/fleet_tracking/<model("fleet.driver"):d>',
    	], auth='public', website=True)
    def index(self,d=None, **kw):
    	driver = http.request.env['fleet.driver']
    	# if d :
    	# 	print("############################333-----------",d)
    	# 	return http.request.render('fleet_tracking.index', {'' : driver.search([])})
    	# else:
    	return http.request.render('fleet_tracking.index', {'driver' : driver.search([])})


    @http.route(['/delete/<model("fleet.driver"):d>',], auth='public', website=True)
    def delete(self,d):
    	d.unlink()
    	return http.request.redirect('/fleet_tracking/')


    @http.route(['/update/<model("fleet.driver"):d>',], auth='public', website=True)
    def update(self,d):
    	# driver = http.request.env['fleet.driver']
    	# did = driver.search([]).browse([d.id])
    	return http.request.render('fleet_tracking.create_update_form', {'driver_id' : d})