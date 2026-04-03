# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class Bobbin(Document):
	"""Bobbin management - tracks rope/wire spools"""
	
	def validate(self):
		"""Validate bobbin"""
		if self.capacity_kg <= 0:
			frappe.throw("Capacity must be greater than 0")
		
		if self.current_load_kg > self.capacity_kg:
			frappe.throw("Current load cannot exceed bobbin capacity")
