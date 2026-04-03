# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class ManufacturingRouting(Document):
	"""Manufacturing Routing - defines sequence of operations"""
	
	def validate(self):
		"""Validate routing"""
		if not self.routing_operations:
			frappe.throw("At least one operation must be defined in the routing")
		
		# Set total operations count
		self.total_operations = len(self.routing_operations)
	
	def on_submit(self):
		"""Actions on submission"""
		pass
