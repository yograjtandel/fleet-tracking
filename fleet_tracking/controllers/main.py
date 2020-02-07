# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
# from fleet_tracking.fleet_vehicle_contract_model import 

class Home(Home):
	def _login_redirect(self, uid, redirect=None):
		if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('fleet_tracking.group_manager'):
			return '/web/'
		if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
			return '/web/'
		if  request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
			return '/home/'
		return super(UserRegister, self)._login_redirect(uid, redirect=redirect)

class UserRegister(http.Controller):
	@http.route('/userregister/', auth="public", type="http", csrf=False)
	def customer_index1(self, **kw):
		currency = http.request.env['res.currency'].sudo().search([]) 
		return http.request.render('fleet_tracking.customer_index1', {'currency': currency}) 
	

	@http.route('/home/',method="post", auth="public", type="http", csrf=False)
	def homepage(self, **post):
		odometer_detail = request.env['fleet.odometer'].sudo().search([])
		return request.render('fleet_tracking.home_page',{'odometer':odometer_detail})
	

	@http.route('/odometer/',method="post", auth="public", type="http", csrf=False)
	def odometer(self, **post):
		vehicle_detail = request.env['fleet.vehicle'].sudo().search([])
		driver_detail = request.env['fleet.driver'].sudo().search([])
		return request.render('fleet_tracking.odometer',{'vehicle' : vehicle_detail,'driver': driver_detail})


	@http.route('/save/odometer/',method="post", auth="public", type="http", csrf=False, website=True)
	def create_update(self,**post):
		print("+++++++++++++++")
		odometer = request.env['fleet.odometer']
		odometer.create({
			'vehicle_id': post.get('vehicle'),
			'driver_id' : post.get('driver'),
			'date' : post.get('date'),
			'odometer_reading' : post.get('reading'),
			'reading_unit' : post.get('unit')})
		return request.redirect('/odometer/')
		
	@http.route('/booking/',method="post", auth="public", type="http", csrf=False)
	def booking(self, **post):
		return request.render('fleet_tracking.contract_booking')
		
	   

	@http.route('/registration/<string:user>',method="post" ,auth="public", type="http", csrf=False) 
	def service_provider_index1(self,user=None, **post):
		if user == 'company': 
			groups_id_name = [(6, 0, [request.env.ref('fleet_tracking.group_manager').id]),(6, 0, [request.env.ref('base.group_user').id])] 
			currency_name = post.get('currency') 
			currency = request.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1) 
			
			partner = request.env['res.partner'].sudo().create({ 
			'name': post.get('username'), 
			'email': post.get('email') }) 
		
			company = request.env['res.company'].sudo().create({ 
			'name': post.get('username'), 
			'partner_id': partner.id, 
			'currency_id': currency.id })

			request.env['res.users'].sudo().create({ 
			'partner_id': partner.id, 
			'login': post.get('username'), 
			'password': post.get('password'),
			'company_id': company.id, 
			'company_ids': [(4, company.id)], 
			'groups_id': groups_id_name }) 
 
		else:

			groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
			partner = request.env['res.partner'].sudo().create({ 
				'name': post.get('username'), 
				'email': post.get('email')})
			request.env['res.users'].sudo().create({ 
				'partner_id': partner.id, 
				'login': post.get('username'), 
				'password': post.get('password'),
				'groups_id': groups_id_name
				})

			request.env['fleet.customer'].sudo().create({
				'name': post.get('username'), 
				'email': post.get('email')
				})
		return http.local_redirect('/web/login?redirect=/homepage') 