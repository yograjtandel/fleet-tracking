# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class  TypeOfMaintenance(models.Model):
	_name = "fleet.maintenance.type"
	_description = "type of maintenance"

	name = fields.Char('Name')
		
class FleetCost(models.Model):
	_name="fleet.cost"
	_description = "manage expence on vehicle"
	
	date = fields.Date('End Date', required=True ,default=fields.Date.today)
	vehicle = fields.Many2one(comodel_name="fleet.vehicle", ondelete="restrict", string="Vehicle")
	maintenance_type = fields.Many2one(comodel_name="fleet.maintenance.type", ondelete="restrict", string='Maintenance Type')
	cost = fields.Float('Cost')
	note = fields.Text('Note')
	
