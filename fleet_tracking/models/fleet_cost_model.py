# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class TypeOfMaintenance(models.Model):
    _name = "fleet.maintenance.type"
    _description = "type of maintenance"

    name = fields.Char('Name')


class FleetCost(models.Model):
    _name = "fleet.cost"
    _description = "manage expence on vehicle"

    date = fields.Date('End Date', required=True, default=fields.Date.today)
    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", ondelete="restrict", string="Vehicle")
    maintenance_type_id = fields.Many2one(comodel_name="fleet.maintenance.type", ondelete="restrict", string='Maintenance Type')
    cost = fields.Float('Cost')
    note = fields.Text('Note')
