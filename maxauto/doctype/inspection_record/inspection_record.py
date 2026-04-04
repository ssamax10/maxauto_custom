# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class InspectionRecord(Document):
	"""Quality inspection records"""
	
	def validate(self):
		"""Validate inspection record"""
		if not self.test_results:
			frappe.throw("At least one test result is required")
		
		# Auto-set result based on test results
		fail_count = sum(1 for row in self.test_results if row.test_result == "Fail")
		if fail_count > 0:
			self.result = "Fail"
		else:
			self.result = "Pass"
