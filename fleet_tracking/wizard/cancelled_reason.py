# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CrmLeadLost(models.TransientModel):
	_name = 'fleet.cancelled.contract'
	_description = 'Get cancelled cancelled Reason'

	cancelled_reason_id = fields.Many2one('fleet.cancelled.reason', 'Cancelled Reason')
	cancelled_date=fields.Date('Cancelled Date' ,default=fields.Date.today)


	def action_cancelled_contract(self):
		contract_env=self.env['fleet.vehicle.contract.booking'].browse(self.env.context.get('active_ids'))
		if contract_env.state == 'renew':
			contract_env=self.env['fleet.contract.renew'].browse(self.env.context.get('active_ids'))
		if self.env.context['state'] in ['draft' , 'confirm']:
			contract_env.write({'state' : 'cancelled'})
			contract_env.cancelled_reason=self.cancelled_reason_id.id
			contract_env.cancelled_date=self.cancelled_date
		else:
			contract_env.write({'state' : 'closed'})
			contract_env.closed_reason=self.cancelled_reason_id.id
			contract_env.closed_date=self.cancelled_date
		return True
