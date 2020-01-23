# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CarModel(models.Model):
	_name = "fleet.vehicle.car.model"
	_description = "vehicle models detail"

	name = fields.Char(name="Model", required=True, help="Ex. Mustang SVT Cobra R.", string="Model Name")
	brand_id = fields.Many2one('fleet.vehicle.brand', 'Manufacturer', required=True, help='Manufacturer of the vehicle')
	image_128 = fields.Image(related='brand_id.image_128', readonly=False, store=True)


class VehicleBrand(models.Model):
	_name = "fleet.vehicle.brand"
	_description = "brand detail of the vehicle"


	name = fields.Char(name="Name", required=True)
	image_128 = fields.Image('image_128' ,max_width=128, max_height=128)




















		

