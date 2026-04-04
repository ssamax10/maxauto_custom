# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class ManufacturingOperationType(Document):
	"""Defines types of manufacturing operations"""
	
	def validate(self):
		"""Validate operation type"""
		if self.external_vendor and not self.vendor_name:
			frappe.throw("Vendor name is required for external processes")
