# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class MachineCapability(Document):
	"""Maps capabilities to machines"""
	
	def validate(self):
		"""Validate machine capability"""
		# Prevent duplicates
		existing = frappe.db.get_value(
			"Machine Capability",
			{"machine": self.machine, "capability_name": self.capability_name},
			"name"
		)
		if existing and existing != self.name:
			frappe.throw(f"Capability already exists for this machine")
