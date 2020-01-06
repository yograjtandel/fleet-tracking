# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
	driver = fields.Many2one(comodel_name='fleet.driver' , ondelete = "set null", string="Driver" )
	no_of_seats = fields.Integer(name="Seats Number")
	no_of_doors = fields.Integer(name="Doors Number")
	color = fields.Char(name="Color", size=15)
	model_year = fields.Char(name="Model Year")
	description = fields.Text(name="Description")
	
	# @api.depends(driver)
	# def _select_driver(self):
	# 	for record in self:
			
