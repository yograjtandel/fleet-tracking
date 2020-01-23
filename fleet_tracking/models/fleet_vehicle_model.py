# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.osv import expression
class  driver(models.Model):
	_name = "fleet.driver"

	name = fields.Char(name = "Driver Name", required=True , string="Driver Name")
	driving_licence_nunmber = fields.Char(name="Driving licence number", required=True)
	phone = fields.Integer(name="phone", required=True)
	email = fields.Char(name="Email")
	address = fields.Text(name="Address")
	image = fields.Image('Image', max_width=90, max_height=90, widget="image")
	birth_date = fields.Date('Birth Date' ,default=fields.Date.today)
	
	@api.constrains('birth_date')
	def _check_age(self):		
		for record in self:
			date = fields.Date.context_today(record)
			if (date.year - record.birth_date.year) < 18:
				raise ValidationError("your age is < 18, you are not eligible for driving")


class FuleType(models.Model):
	_name="fleet.vehicle.fule.type"
	_description="type of fule"

	name= fields.Char('Fule Type')


class vehicle(models.Model):
	_name = "fleet.vehicle"
	_description = "vehicle detail"

	_rec_name = "license_plate"
	model_id = fields.Many2one(comodel_name='fleet.vehicle.car.model', string='Model',
        tracking=True, required=True, help='Model of the vehicle')
	license_plate = fields.Char(name = "license plate")
	no_of_seats = fields.Integer(name="Seats Number")
	no_of_doors = fields.Integer(name="Doors Number")
	color = fields.Char(name="Color", size=15)
	model_year = fields.Char(name="Model Year")
	description = fields.Text(name="Description")
	fule_type = fields.Many2one(comodel_name="fleet.vehicle.fule.type", ondelete="restrict", string="Fule Type")
	contract_id = fields.Many2one(comodel_name="fleet.vehicle.trip.booking")
	image_128 = fields.Image(related='model_id.image_128', readonly=False, store=True)

