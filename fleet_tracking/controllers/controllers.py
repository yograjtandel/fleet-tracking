# -*- coding: utf-8 -*-
from odoo import http

class Academy(http.Controller):
    @http.route('/fleet_tracking/', auth='public', website=True)
    def index(self, **kw):
    	driver = http.request.env['fleet.driver']
    	return http.request.render('fleet_tracking.index', {'driver' : driver.search([])})