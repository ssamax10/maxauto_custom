# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class ClosingBatch(Document):
	"""Closing batch - tracks rope closing"""
	
	def calculate_total_input(self):
		"""Calculate total input quantity"""
		total = sum([row.qty for row in self.input_strands])
		self.total_input_qty_kg = total
	
	def validate(self):
		"""Validate closing batch"""
		self.calculate_total_input()
		
		if not self.input_strands:
			frappe.throw("At least one input strand is required")
	
	def on_submit(self):
		"""Update machine and create inventory"""
		frappe.db.set_value("Machine", self.closing_machine, "status", "Operational")
