# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CarModel(models.Model):
    _name = "fleet.vehicle.car.model"
    _table = 'fleet_vehicle_custom_table'
    _description = "vehicle models detail"

    name = fields.Char(name="Model", required=True, help="Ex. Mustang SVT Cobra R.", string="Model Name")
    brand_id = fields.Many2one('fleet.vehicle.brand', 'Manufacturer', required=True, help='Manufacturer of the vehicle')
    image_128 = fields.Image(related='brand_id.image_128', readonly=False, store=True)

    def name_get(self):
        name = []
        for model in self:
            name.append((model.id, str(model.brand_id.name)+"-"+str(model.name)))
        return name


class VehicleBrand(models.Model):
    _name = "fleet.vehicle.brand"
    _description = "brand detail of the vehicle"

    name = fields.Char(name="Name", required=True)
    active = fields.Boolean(default=True)
    image_128 = fields.Image('image_128', max_width=128, max_height=128)

    @api.model
    def abc(self, **args):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
