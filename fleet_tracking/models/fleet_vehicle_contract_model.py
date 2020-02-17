# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import json
from collections import Counter
from passlib.context import CryptContext


class Customer(models.Model):
    _name = "fleet.customer"
    _description = "customer detail"

    name = fields.Char(name="Name")
    email = fields.Char(name="Email")
    mobile = fields.Char(name="Mobile")
    street1 = fields.Char(name="Street1")
    street2 = fields.Char(name="Street2")
    city = fields.Char(name="City")
    state = fields.Many2one(comodel_name="fleet.state", string="State")
    pincode = fields.Char(name="Pincode")
    country = fields.Char(name="Notes")
    trip_id = fields.Many2one(comodel_name="fleet.vehicle.contract.trip")
    password = fields.Char(name="password")
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=10, index=True)

    @api.model
    def create(self, vals):
        if not self.env['res.users'].search([('login', '=', vals.get('name'))]):
            groups_id_name = [(6, 0, [self.env.ref('fleet_tracking.group_customer').id])]
            partner = self.env['res.partner'].create({
                            'name': vals.get('name'),
                            'email': vals.get('email')})
            self.env['res.users'].create({
                'partner_id': partner.id,
                'login': vals.get('name'),
                'password': vals.get('password'),
                'groups_id': groups_id_name})

        pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000
        )
        print(vals['password'])
        vals['password'] = pwd_context.encrypt(vals['password'])

        return super(Customer, self).create(vals)


class VehicleContract(models.Model):
    _name = "fleet.vehicle.contract.booking"
    _description = "service tpye of the vehicle"
    _rec_name = "customer_id"

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    customer_id = fields.Many2one(string="Customer Name", comodel_name="fleet.customer", required=True)
    start_date = fields.Date('Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date('End Date', required=True, default=fields.Date.today)
    duration = fields.Char('Duration', compute="_compute_duration", default=0)
    instruction = fields.Text(name="Other Instruction")
    state = fields.Selection(selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('cancelled', 'Cancelled'), ('running', 'Running'), ('closed', 'Closed'), ('renew', 'ReNew')], default='draft')
    required_vehicle_ids = fields.Many2many(comodel_name="fleet.vehicle", compute="_compute_available_vehicle", string='not Vehicle')
    vehicle_ids = fields.Many2many(comodel_name="fleet.vehicle", domain="[('id', 'in', required_vehicle_ids)]", string='Vehicle', required=True)
    count_trips = fields.Integer(compute="_count_trips")
    model_id = fields.Many2one('fleet.vehicle.car.model', 'Model')
    image_128 = fields.Image(related='model_id.image_128', readonly=False)
    cancelled_reason_id = fields.Many2one(comodel_name="fleet.cancelled.reason", string="Cancelled Reason")
    cancelled_date = fields.Date('Cancelled Date', default=None)
    closed_reason_id = fields.Many2one(comodel_name="fleet.cancelled.reason", string="Closed Reason")
    closed_date = fields.Date('Closed Date', default=None)
    kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')
    renew_detail = fields.One2many(comodel_name="fleet.contract.renew", inverse_name='contract_id', string="ReNew", stored=False)

    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        for record in self:
            record.duration = (record.end_date - record.start_date).days + 1

    def _count_trips(self):
        trip_env = self.env['fleet.vehicle.contract.trip']
        for record in self:
            record.count_trips = trip_env.search_count([('contract_id', '=', record.id)])

    def open_trip(self):
        if self.count_trips > 0:
            if self.state in ['confirm', 'running']:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Assignation Logs',
                    'view_type': 'list',
                    'view_mode': 'list,form',
                    'res_model': 'fleet.vehicle.contract.trip',
                    'domain': [('contract_id', '=', self.id)],
                    'context': {'default_contract_id': self.id}
                }
            if self.state in ['closed', 'renew']:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Assignation Logs',
                    'view_type': 'list',
                    'view_mode': 'list',
                    'res_model': 'fleet.vehicle.contract.trip',
                    'domain': [('contract_id', '=', self.id)],
                }
        else:
            if self.state in ['confirm', 'running']:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'New Trip',
                    'view_mode': 'form',
                    'res_model': 'fleet.vehicle.contract.trip',
                    'context': {'default_contract_id': self.id}
                }

    @api.depends("start_date", "end_date")
    def _compute_available_vehicle(self):

        booking_env1 = self.env['fleet.vehicle.contract.booking'].search(['&', ('state', '!=', 'cancelled'), '|', '&', ('start_date', '<=', self.start_date), ('end_date', '>=', self.start_date),
                                                                          '&', ('start_date', '<=', self.end_date), ('end_date', '>=', self.end_date)])

        booking_renew_env1 = self.env['fleet.contract.renew'].search(['&', ('state', '!=', 'cancelled'), '|', '&', ('start_date', '<=', self.start_date), ('end_date', '>=', self.start_date),
                                                                      '&', ('start_date', '<=', self.end_date), ('end_date', '>=', self.end_date)])

        vehicle_list = booking_env1.filtered(lambda con: con.state in ['confirm', 'running']).mapped('vehicle_ids.id')
        vehicle_list += booking_renew_env1.filtered(lambda con: con.state in ['confirm', 'running']).mapped('vehicle_ids.id')

        self.required_vehicle_ids = self.env['fleet.vehicle'].search([('id', 'not in', vehicle_list)])

    def action_confirm(self):
        self.write({'state': 'confirm'})
        return True

    def action_draft(self):
        self.write({'state': 'draft'})
        return True

    def action_running(self):
        self.write({'state': 'running'})
        return True

    def action_renew_contract(self, **args):
        return {
            'type': 'ir.actions.act_window',
            'name': 'ReNew Contract',
            'view_mode': 'form',
            'res_model': 'fleet.contract.renew',
            'target': 'new',
            'context': {'default_contract_id': self.id,
                        'default_instruction': self.instruction,
                        }
        }

    @api.constrains('start_date', 'end_date')
    def _check_validity_of_date(self):
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError("Contract end date must be greter than start date")

    def _kanban_dashboard_graph(self):
        for journal in self:
            journal.kanban_dashboard_graph = json.dumps(journal.get_bar_graph_datas())

    def get_bar_graph_datas(self):
        data = []
        contract_env = self.env['fleet.vehicle.contract.booking'].search([])

        list_of_date = [date.start_date.strftime("%m") for date in contract_env]
        data_values = Counter(list_of_date)
        for key in data_values:
            data.append({'label': key, 'value': data_values[key], 'type': 'past'})

        return [{'values': data, 'title': "Monthly Contract", 'key': "graph_key", 'is_sample_data': True}]


class ContractTrip(models.Model):
    _name = "fleet.vehicle.contract.trip"
    _description = "trip detail related to contract"
    _rec_name = "contract_id"

    date = fields.Date('Date', required=True, default=fields.Date.today)
    contract_id = fields.Many2one(comodel_name="fleet.vehicle.contract.booking", string="Contract Id", domain="[('state','not in',['cancelled','draft'])]")
    driver_id = fields.Many2one(comodel_name="fleet.driver", ondelete="restrict", string='Driver Id')
    distance_travelled = fields.Float(name="Distance")
    no_of_person_in_trip = fields.Integer(name="No of Person")
    address_ids = fields.Many2many(comodel_name='fleet.trip.address', string="Address")
    renew_id = fields.Many2one(comodel_name='fleet.contract.renew', string="Renew ID")


class State(models.Model):
    _name = "fleet.state"
    _description = "list of state"
    name = fields.Char(name="State Name")


class Address(models.Model):
    _name = "fleet.trip.address"
    _description = "address included in trip"

    _rec_name = "street1"
    street1 = fields.Char(name="Street1")
    street2 = fields.Char(name="Street2")
    city = fields.Char(name="City")
    state_id = fields.Many2one(comodel_name="fleet.state", string="State")
    pincode = fields.Char(name="Pincode")
    notes = fields.Text(name="Notes")


class CancelledReason(models.Model):
    _name = "fleet.cancelled.reason"
    _description = "contract calcel reason"

    name = fields.Char(name="Reason", required=True)
    reason_type = fields.Boolean("Reason Type")


class ContractRenew(models.Model):
    _name = "fleet.contract.renew"
    _description = "detail of renew contract"

    contract_id = fields.Many2one(comodel_name="fleet.vehicle.contract.booking", string="Contract Id")
    renew_date = fields.Date('Renew Date', default=fields.Date.today)
    start_date = fields.Date('Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date('End Date', required=True, default=fields.Date.today)
    duration = fields.Char('Duration', compute="_compute_duration")
    required_vehicle_ids = fields.Many2many(comodel_name="fleet.vehicle", compute="_compute_available_vehicle", string='not Vehicle')
    vehicle_ids = fields.Many2many(comodel_name="fleet.vehicle", domain="[('id', 'in',required_vehicle_ids)]", string='Vehicle', required=True)
    instruction = fields.Text(name="Other Instruction")
    state = fields.Selection(selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('cancelled', 'Cancelled'), ('running', 'Running'), ('closed', 'Closed'), ('renew', 'ReNew')], default='draft')
    count_trips = fields.Integer(compute="_count_trips")

    @api.model
    def create(self, vals):
        self.env["fleet.vehicle.contract.booking"].browse([vals['contract_id']]).write({'state': 'renew'})
        return super(ContractRenew, self).create(vals)

    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        if self.start_date and self.end_date:
            for record in self:
                record.duration = (record.end_date - record.start_date).days + 1
        else:
            self.duration = 0

    @api.depends("start_date", "end_date")
    def _compute_available_vehicle(self):

        booking_env1 = self.env['fleet.vehicle.contract.booking'].search(['&', ('state', '!=', 'cancelled'), '|', '&', ('start_date', '<=', self.start_date), ('end_date', '>=', self.start_date),
                                                                          '&', ('start_date', '<=', self.end_date), ('end_date', '>=', self.end_date)])

        booking_renew_env1 = self.env['fleet.contract.renew'].search(['&', ('state', '!=', 'cancelled'), '|', '&', ('start_date', '<=', self.start_date), ('end_date', '>=', self.start_date),
                                                                      '&', ('start_date', '<=', self.end_date), ('end_date', '>=', self.end_date)])

        vehicle_list = booking_env1.filtered(lambda con: con.state in ['confirm', 'running']).mapped('vehicle_ids.id')
        vehicle_list += booking_renew_env1.filtered(lambda con: con.state in ['confirm', 'running']).mapped('vehicle_ids.id')

        self.required_vehicle_ids = self.env['fleet.vehicle'].search([('id', 'not in', vehicle_list)])

    def open_trip(self):
        if self.count_trips > 0:
            if self.state in ['confirm', 'running']:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Assignation Logs',
                    'view_type': 'list',
                    'view_mode': 'list,form',
                    'res_model': 'fleet.vehicle.contract.trip',
                    'domain': [('contract_id', '=', self.id)],
                    'context': {'default_contract_id': self.id}
                }
            if self.state in ['closed', 'renew']:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Assignation Logs',
                    'view_type': 'list',
                    'view_mode': 'list',
                    'res_model': 'fleet.vehicle.contract.trip',
                    'domain': [('contract_id', '=', self.id)],
                }
        else:
            if self.state in ['confirm', 'running']:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'New Trip',
                    'view_mode': 'form',
                    'res_model': 'fleet.vehicle.contract.trip',
                    'context': {'default_contract_id': self.id}
                }

    def _count_trips(self):
        trip_env = self.env['fleet.vehicle.contract.trip']
        for record in self:
            record.count_trips = trip_env.search_count([('contract_id', '=', record.contract_id.id), ('renew_id', '=', record.id)])

    def action_renew_contract(self, **args):
        return {
            'type': 'ir.actions.act_window',
            'name': 'ReNew Contract',
            'view_mode': 'form',
            'res_model': 'fleet.contract.renew',
            'target': 'new',
            'context': {'default_contract_id': self.id,
                        'default_instruction': self.instruction,
                        'default_vehicle_id': self.vehicle_id.ids
                        }
        }

    def action_draft(self):
        self.write({'state': 'draft'})
        return True

    def action_confirm(self):
        self.write({'state': 'confirm'})
        return True

    def action_running(self):
        self.write({'state': 'running'})
        return True
