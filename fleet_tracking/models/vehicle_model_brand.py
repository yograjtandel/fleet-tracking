# -*- coding: utf-8 -*-

from odoo import models, fields, api

class VehicleBrand(models.Model):
	_name = "vehicle.brand"
	_description = "brand detail of the vehicle"


	name = fields.Char(name="Name", required=True)


class CarModel(models.Model):
	_name = "vehicle.car.model"
	_description = "vehicle models detail"

	name = fields.Char(name="Name", required=True, help="Ex. Mustang SVT Cobra R.")
	brand_name = fields.Many2one(comodel_name='vehicle.brand', ondelete = "set null", string="Brand")


class vehicle(models.Model):
	_name = "vehicle.vehicle"
	_description = "vehicle detail"

	# name = fields.Char(name="name")
	name = fields.Many2one(comodel_name='vehicle.car.model', ondelete = "set null", string="Vehicle")
	license_plate = fields.Char(name = "license plate")
