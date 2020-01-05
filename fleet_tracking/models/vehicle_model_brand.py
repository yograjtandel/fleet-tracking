# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VehicleBrand(models.Model):
	_name = "fleet.vehicle.brand"
	_description = "brand detail of the vehicle"


	name = fields.Char(name="Name", required=True)


class CarModel(models.Model):
	_name = "fleet.vehicle.car.model"
	_description = "vehicle models detail"

	name = fields.Char(name="Model", required=True, help="Ex. Mustang SVT Cobra R.", string="Model Name")
	brand_name = fields.Many2one(comodel_name='fleet.vehicle.brand', ondelete = "restrict", string="Brand")


class  driver(models.Model):
	_name = "fleet.driver"

	name = fields.Char(name = "Driver Name", required=True , string="Driver Name")
	address = fields.Text(name="Address", required=True)
	phone = fields.Integer(name="phone", required=True)
	email = fields.Char(name="Email")
	birth_date = fields.Date('Birth Date', required=True ,default=fields.Date.today)

	@api.constrains('birth_date')
	def _check_age(self):		
		for record in self:
			date = fields.Date.context_today(record)
			if (date.year - record.birth_date.year) < 18:
				raise ValidationError("your age is < 18, you are not eligible for driving")


class vehicle(models.Model):
	_name = "fleet.vehicle"
	_description = "vehicle detail"

	_rec_name = "license_plate"
	# name = fields.Char(name="name")
	model = fields.Many2one(comodel_name='fleet.vehicle.car.model', ondelete = "restrict", string="Model Name")
	license_plate = fields.Char(name = "license plate")
	driver = fields.Many2one(comodel_name='fleet.driver' , ondelete = "restrict", string="Driver")
	no_of_seats = fields.Integer(name="Seats Number")
	no_of_doors = fields.Integer(name="Doors Number")
	color = fields.Char(name="Color", size=15)
	model_year = fields.Char(name="Model Year")
	description = fields.Text(name="Description")





class VehicleServiceType(models.Model):
	_name = "fleet.vehicle.service.type"
	_description = "service tpye of the vehicle"

	name = fields.Char(name="Service Type", required=True)
		




class VehicleService(models.Model):
	_name = "fleet.vehicle.service"
	_description = "service of the vehicle"

	name = fields.Many2one(comodel_name='fleet.vehicle.service.type',string="Service Tpye",required=True, ondelete="restrict")
	date = fields.Date('Service Date', required=True ,default=fields.Date.today)
	cost = fields.Float('Cost')
	vehicle = fields.Many2one(comodel_name='fleet.vehicle',required=True,ondelete = "restrict", string="Vehicle")
	note = fields.Text(name="Note")



class customer(models.Model):
	_name = "fleet.customer"
	_description = "customer detail"

	name = fields.Char(name="Name")
	email = fields.Char(name="Email")
	mobile = fields.Integer(name="Mobile")

class ContractType(models.Model):
	_name = "contract.type"
	_description = "contract type"

	name = fields.Char(name="Contarct Type")

class VehicleContract(models.Model):
	_name = "fleet.vehicle.contract"
	_description = "service tpye of the vehicle"


	name = fields.Many2one(string="Name", comodel_name="fleet.customer")
	contract_type = fields.Many2one(comodel_name="contract.type", ondelete="restrict", string="Contarct Type")
	start_date = fields.Date('Start Date', required=True ,default=fields.Date.today)
	end_date = fields.Date('End Date', required=True ,default=fields.Date.today)
	vehicle = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle")
	instruction = fields.Text(name="Instruction")

	@api.constrains('start_date' , 'end_date')
	def _check_age(self):		
		for record in self:
			if record.end_date < record.start_date:
				raise ValidationError("invalid dates")







		

