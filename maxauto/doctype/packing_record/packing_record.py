# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class PackingRecord(Document):
	"""Packing records for finished goods"""
	
	def validate(self):
		"""Validate packing record"""
		if self.quantity <= 0:
			frappe.throw("Quantity must be greater than 0")
		
		if self.total_weight_kg and self.total_weight_kg <= 0:
			frappe.throw("Total weight must be greater than 0")
	
	def on_submit(self):
		"""Create stock movement on packing"""
		pass
