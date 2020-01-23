import json
import datetime
from odoo import models, api, _, fields
from collections import Counter



class FleetDashboard(models.Model):
	_name = "fleet.dashboard"
	_description="dashboard"

	kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph',store=True)

	def _kanban_dashboard_graph(self):
		for journal in self:
			journal.kanban_dashboard_graph = json.dumps(journal.get_bar_graph_datas())
		print("###########",journal.kanban_dashboard_graph)

		

	def get_bar_graph_datas(self):
		data =[]
		data.append({'label': _('month'), 'value':0.0, 'type': 'past'})
		contract_env = self.env['fleet.vehicle.contract.booking'].search([])

		list_of_date=[date.start_date.strftime("%m") for date in contract_env]
		data_values = Counter(list_of_date)
		print("___________________________",data_values)
		for key in data_values:
			print("key",key)
			data.append({'label':key, 'value':data_values[key], 'type': 'past'})

		print("+++++++++++++++++++++++++++",data)
		return [{'values': data, 'title': "Monthly Contract", 'key': "graph_key", 'is_sample_data': True}]
	
	