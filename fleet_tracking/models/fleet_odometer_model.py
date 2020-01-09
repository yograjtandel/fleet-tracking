# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class odometer(models.Model):
	_name = 'fleet.odometer'
	_description = "odometer"

	_rec_name="vehicle_id"
	vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", ondelete="restrict", string="Vehicle")
	date = fields.Date('Date', required=True ,default=fields.Date.today)
	driver_id = fields.Many2one(comodel_name="fleet.driver",ondelete="restrict", string="Driver")
	odometer_reading = fields.Float('Odometer')
	reading_unit = fields.Char('unit' , default="Km")

	@api.model
	def create(self, vals):
		print("\n\n\n\n\n\n")
		print("########################################3",vals)
		
		return super(odometer, self).create(vals)

	def write(self, vals):
		# print("####################",self.env['fleet.odometer'].search([('odometer_reading', '=', "223.00")]))
		print("####################",self.env['fleet.odometer'].browse([3])._context)
		return super(odometer, self).write(vals)

	def unlink(self):
		print("-----------------------")
		super(odometer,self).unlink()

	def copy(self,default=None):
		print("$$$$$$$$$$$$$$$$$$$$$$444")
		return super(odometer,self).copy(default)