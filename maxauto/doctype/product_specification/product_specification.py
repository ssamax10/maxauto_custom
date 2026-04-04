# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT
# See license.txt

import frappe
from frappe.model.document import Document


class ProductSpecification(Document):
	"""Product Specification DocType for rope/cable products"""
	
	def validate(self):
		"""Validate product specifications"""
		if self.wire_diameter and self.wire_diameter <= 0:
			frappe.throw("Wire diameter must be greater than 0")
		
		if self.strand_count and self.strand_count <= 0:
			frappe.throw("Strand count must be greater than 0")
		
		if self.breaking_load and self.breaking_load <= 0:
			frappe.throw("Breaking load must be greater than 0")
