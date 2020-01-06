# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

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