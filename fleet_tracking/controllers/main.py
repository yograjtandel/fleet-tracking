# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
import werkzeug


class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('fleet_tracking.group_manager'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
            return '/my/'
        return super(UserRegister, self)._login_redirect(uid, redirect=redirect)


class UserRegister(http.Controller):
    @http.route('/userregister/', auth="public", type="http", csrf=False)
    def customer_index1(self, **kw):
        currency = http.request.env['res.currency'].sudo().search([])
        return http.request.render('fleet_tracking.customer_index1', {'currency': currency})

    @http.route('/my/', method="post", auth="user", type="http")
    def homepage(self, **post):
        print("+++++++", request.session['login'])
        # print("+++++++++++++++++\n\n\n\n", request.env.user.has_group('fleet_tracking.group_driver'))
        odometer_detail = request.env['fleet.odometer'].sudo().search([])
        return request.render('fleet_tracking.home_page', {'odometer': odometer_detail})

    @http.route('/odometer/', method="post", auth="user", type="http", csrf=False)
    def odometer(self, **post):
        vehicle_detail = request.env['fleet.vehicle'].sudo().search([])
        driver_detail = request.env['fleet.driver'].sudo().search([])
        return request.render('fleet_tracking.odometer', {'vehicle': vehicle_detail, 'driver': driver_detail})

    @http.route('/save/odometer/', method="post", auth="user", type="http", website=True, csrf=False)
    def create_update(self, **post):
        odometer = request.env['fleet.odometer']
        odometer.create({'vehicle_id': post.get('vehicle'),
                         'driver_id': post.get('driver'),
                         'date': post.get('date'),
                         'odometer_reading': post.get('reading'),
                         'reading_unit': post.get('unit')})
        return werkzeug.unils.redirect('/odometer/')

    @http.route('/map/', method="post", auth="user", type="http", csrf=False)
    def map(self, **post):
        return request.render('fleet_tracking.render_map')

    @http.route('/contract/', method="post", auth="user", type="http", csrf=False)
    def booking(self, **post):
        vehicles = None
        if post.get('start_date') and post.get('end_date'):

            booking_env1 = request.env['fleet.vehicle.contract.booking'].search(['&', ('state', '!=', 'cancelled'), '|', '&', ('start_date', '<=', post.get('start_date')), ('end_date', '>=', post.get('start_date')),
                                                                                 '&', ('start_date', '<=', post.get('end_date')), ('end_date', '>=', post.get('end_date'))])

            booking_renew_env1 = request.env['fleet.contract.renew'].search(['&', ('state', '!=', 'cancelled'), '|', '&', ('start_date', '<=', post.get('start_date')), ('end_date', '>=', post.get('start_date')),
                                                                             '&', ('start_date', '<=', post.get('end_date')), ('end_date', '>=', post.get('end_date'))])

            vehicle_list = booking_env1.filtered(lambda con: con.state in ['confirm', 'running']).mapped('vehicle_ids.id')
            vehicle_list += booking_renew_env1.filtered(lambda con: con.state in ['confirm', 'running']).mapped('vehicle_ids.id')

            vehicles = request.env['fleet.vehicle'].search([('id', 'not in', vehicle_list)])
            return request.render('fleet_tracking.contract_booking', {'vehicles': vehicles,
                                                                      'start_date': post.get('start_date'),
                                                                      'end_date': post.get('end_date')})
        return request.render('fleet_tracking.contract_booking', {'vehicles': vehicles})

    @http.route('/registration/<string:user>', method="post", auth="public", type="http", csrf=False)
    def service_provider_index1(self, user=None, **post):
        if user == 'company':
            groups_id_name = [(6, 0, [request.env.ref('fleet_tracking.group_manager').id])]
            currency_name = post.get('currency')
            currency = request.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1)

            partner = request.env['res.partner'].sudo().create({'name': post.get('username'),
                                                                'email': post.get('email')})

            company = request.env['res.company'].sudo().create({'name': post.get('username'),
                                                                'partner_id': partner.id,
                                                                'currency_id': currency.id})

            request.env['res.users'].sudo().create({'partner_id': partner.id,
                                                    'login': post.get('username'),
                                                    'password': post.get('password'),
                                                    'company_id': company.id,
                                                    'company_ids': [(4, company.id)],
                                                    'groups_id': groups_id_name})

        else:

            groups_id_name = [(6, 0, [request.env.ref('fleet_tracking.group_customer').id])]
            partner = request.env['res.partner'].sudo().create({'name': post.get('username'),
                                                                'email': post.get('email')})
            request.env['res.users'].sudo().create({'partner_id': partner.id,
                                                    'login': post.get('username'),
                                                    'password': post.get('password'),
                                                    'groups_id': groups_id_name})

            request.env['fleet.customer'].sudo().create({'name': post.get('username'),
                                                         'email': post.get('email'),
                                                         'password': post.get('password')})
        return http.local_redirect('/web/login?redirect=/homepage')
