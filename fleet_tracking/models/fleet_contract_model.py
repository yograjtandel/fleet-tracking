# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
				raise ValidationError("Contract end date must be greter than start date")
