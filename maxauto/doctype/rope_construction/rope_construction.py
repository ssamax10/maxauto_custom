# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class RopeConstruction(Document):
	"""Rope construction master - defines rope types"""
	
	def validate(self):
		"""Validate rope construction parameters"""
		if self.strand_count <= 0:
			frappe.throw("Strand count must be greater than 0")
		if self.wires_per_strand <= 0:
			frappe.throw("Wires per strand must be greater than 0")
