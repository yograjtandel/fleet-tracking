# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json
import datetime
from collections import Counter
class customer(models.Model):
	_name = "fleet.customer"
	_description = "customer detail"

	name = fields.Char(name="Name")
	email = fields.Char(name="Email")
	mobile = fields.Integer(name="Mobile")

	street1 = fields.Char(name="Street1")
	street2 = fields.Char(name="Street2")
	city =fields.Char(name="City")
	state=fields.Many2one(comodel_name="fleet.state", string="State")
	pincode=fields.Char(name="Pincode")
	notes=fields.Text(name="Notes")
	trip_id=fields.Many2one(comodel_name="fleet.vehicle.contract.trip")


		
class VehicleContract(models.Model):
	_name = "fleet.vehicle.contract.booking"
	_description = "service tpye of the vehicle"

	_rec_name = "customer"
	customer = fields.Many2one(string="Customer Name", comodel_name="fleet.customer", required=True)
	# contract_type = fields.Many2one(comodel_name="contract.type", ondelete="restrict", string="Contarct Type")
	start_date = fields.Date('Start Date', required=True ,default=fields.Date.today)
	end_date = fields.Date('End Date', required=True ,default=fields.Date.today)
	duration = fields.Char('Duration', compute="_compute_duration")
	instruction = fields.Text(name="Other Instruction")
	state = fields.Selection(selection = [('draft','Draft'),('confirm','Confirm'),('done','Done')],default = 'draft')	
	not_required_vehicle_ids = fields.Many2many(comodel_name="fleet.vehicle",compute="_compute_available_vehicle", string='not Vehicle')
	vehicle_id = fields.Many2many(comodel_name="fleet.vehicle",domain="[('id', 'in',not_required_vehicle_ids)]", string='Vehicle', required=True)
	count_trips = fields.Integer(compute="_count_trips")
	model_id = fields.Many2one('fleet.vehicle.car.model', 'Model',
		tracking=True, help='Model of the vehicle')
	image_128 = fields.Image(related='model_id.image_128', readonly=False)
	
	@api.depends("start_date","end_date")
	def _compute_duration(self):
		for record in self:
			record.duration = (record.end_date - record.start_date)
	

	def _count_trips(self):
		trip_env = self.env['fleet.vehicle.contract.trip']
		for record in self:
			record.count_trips = trip_env.search_count([('contract_id', '=', record.id)])

	def open_trip(self):
		if self.count_trips > 0:
			return {
				'type': 'ir.actions.act_window',
				'name': 'Assignation Logs',
				'view_mode': 'tree',
				'res_model': 'fleet.vehicle.contract.trip',
				'domain': [('contract_id', '=', self.id)],
			}
		else:
			return {
				'type': 'ir.actions.act_window',
				'name': 'New Trip',
				'view_mode': 'form',
				'res_model': 'fleet.vehicle.contract.trip',

				'context': {'default_contract_id': self.id}
			}

	# @api.onchange("start_date","end_date")
	# def _onchange_dates(self):
	# 	booking_env = self.env['fleet.vehicle.contract.booking'].search([])
	# 	vehicle_env = self.env['fleet.vehicle'].search([])


	# 	booking_e = self.env['fleet.vehicle.contract.booking'].search(['|',('start_date','<=',self.start_date),('end_date','>=',self.start_date),
	# 																('start_date','<=',self.end_date),('end_date','>=',self.end_date)])
	# 	# d_list=[]
	# 	# for dt in booking_e:
	# 	# 	d_list.append(dt.start_date)
	# 	# print(d_list)	
	# 	print("++++++++++++",booking_e)
	# 	# booking_env1=self.env['fleet.vehicle.contract.booking'].search([('end_date','<',min(booking_e.start_date))])
	# 	vehicle_list= [v_id for v_id in booking_e.vehicle_id.ids]
	# 	print("$$$$$$$$$$$$",self.mapped(self.vehicle_id))
	# 	print("!!!!!!!!!!!!!!!!!",vehicle_list)
	# 	return {'domain': {'vehicle_id': [('id', 'not in',vehicle_list)]}}

	@api.depends("start_date","end_date")
	def _compute_available_vehicle(self):
		booking_env = self.env['fleet.vehicle.contract.booking'].search([])
		vehicle_env = self.env['fleet.vehicle'].search([])


		booking_e = self.env['fleet.vehicle.contract.booking'].search(['|',('start_date','<=',self.start_date),('end_date','>=',self.start_date),
																	('start_date','<=',self.end_date),('end_date','>=',self.end_date)])

		vehicle_list= [v_id for v_id in booking_e.vehicle_id.ids]
		print("!!!!!!!!!!!!!!!!!",vehicle_list)
		self.not_required_vehicle_ids=self.env['fleet.vehicle'].search([('id', 'not in',vehicle_list)])


	def action_confirm(self):
		self.write({'state' : 'confirm'})
		return True


	def action_draft(self):
		self.write({'state' : 'draft'})
		return True


	def action_done(self):
		self.write({'state' : 'done'})
		return True


	@api.constrains('start_date' , 'end_date')
	def _check_validity_of_date(self):		
		for record in self:
			if record.end_date < record.start_date:
				raise ValidationError("Contract end date must be greter than start date")


	def _kanban_dashboard_graph(self):
		for journal in self:
			journal.kanban_dashboard_graph = json.dumps(journal.get_bar_graph_datas())
		# print("###########",journal.kanban_dashboard_graph)

		

	def get_bar_graph_datas(self):
		data =[]
		data.append({'label': _('month'), 'value':0.0, 'type': 'past'})
		contract_env = self.env['fleet.vehicle.contract.booking'].search([])

		list_of_date=[date.start_date.strftime("%m") for date in contract_env]
		data_values = Counter(list_of_date)
		# print("___________________________",data_values)
		for key in data_values:
			print("key",key)
			data.append({'label':key, 'value':data_values[key], 'type': 'past'})

		# print("+++++++++++++++++++++++++++",data)
		return [{'values': data, 'title': "Monthly Contract", 'key': "graph_key", 'is_sample_data': True}]
	
	kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')

class ContractVehicle(models.Model):
	_name="fleet.contract.vehicle"
	_description="relation between contract and vehicle"

	contract_id=fields.Many2one(comodel_name="leet.vehicle.contract.booking", string="Contract Id")

class ContractTrip(models.Model):
	_name="fleet.vehicle.contract.trip"
	_description="trip detail related to contract"
	_rec_name = "contract_id"

	date = fields.Date('Date', required=True ,default=fields.Date.today)
	contract_id=fields.Many2one(comodel_name="fleet.vehicle.contract.booking",string="Contract Id")
	driver_id = fields.Many2one(comodel_name="fleet.driver", ondelete="restrict",string= 'Driver Id')
	distance_travelled = fields.Float(name="Distance")
	no_of_person_in_trip=fields.Integer(name="No of Person")
	address = fields.One2many(comodel_name='fleet.vehicle.contract.trip.address' , inverse_name ='trip_id', string="Address")


class State(models.Model):
	_name="fleet.state"
	_description="list of state"	

	name=fields.Char(name="State Name")

class Address(models.Model):
	_name = "fleet.vehicle.contract.trip.address"
	_description = "address included in trip"

	_rec_name= "street1"
	street1 = fields.Char(name="Street1")
	street2 = fields.Char(name="Street2")
	city =fields.Char(name="City")
	state=fields.Many2one(comodel_name="fleet.state", string="State")
	pincode=fields.Char(name="Pincode")
	notes=fields.Text(name="Notes")
	trip_id=fields.Many2one(comodel_name="fleet.vehicle.contract.trip")