# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VehicleBrand(models.Model):
	_name = "fleet.vehicle.brand"
	_description = "brand detail of the vehicle"


	name = fields.Char(name="Name", required=True)
	logo = fields.Image('logo' ,max_width=128, max_height=128)


class CarModel(models.Model):
	_name = "fleet.vehicle.car.model"
	_description = "vehicle models detail"

	name = fields.Char(name="Model", required=True, help="Ex. Mustang SVT Cobra R.", string="Model Name")
	brand_name = fields.Many2one(comodel_name='fleet.vehicle.brand', ondelete = "restrict", string="Brand")



















		

