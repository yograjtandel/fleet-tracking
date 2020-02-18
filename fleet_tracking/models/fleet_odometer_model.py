# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class odometer(models.Model):
    _name = 'fleet.odometer'
    _description = "odometer"

    _rec_name = "vehicle_id"
    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", ondelete="restrict", string="Vehicle")
    date = fields.Date('Date', required=True, default=fields.Date.today)
    driver_id = fields.Many2one(comodel_name="fleet.driver", ondelete="restrict", string="Driver")
    odometer_reading = fields.Float('Odometer')
    reading_unit = fields.Char('Unit', default="Km")
