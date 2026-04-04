# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class StrandingBatch(Document):
	"""Stranding batch - tracks strand creation"""
	
	def calculate_total_input(self):
		"""Calculate total input quantity"""
		total = sum([row.qty for row in self.input_bobbins])
		self.total_input_qty_kg = total
	
	def validate(self):
		"""Validate stranding batch"""
		self.calculate_total_input()
		
		if not self.input_bobbins:
			frappe.throw("At least one input bobbin is required")
	
	def on_submit(self):
		"""Update machine status when batch submitted"""
		frappe.db.set_value("Machine", self.stranding_machine, "status", "Operational")
