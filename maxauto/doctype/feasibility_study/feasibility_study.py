# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT
# See license.txt

import frappe
from frappe.model.document import Document


class FeasibilityStudy(Document):
	"""Feasibility Study for engineering projects"""
	
	def validate(self):
		"""Validate feasibility study"""
		if self.cycle_time_estimate and self.cycle_time_estimate <= 0:
			frappe.throw("Cycle time must be greater than 0")
	
	def on_submit(self):
		"""Update project status when feasibility approved"""
		if self.study_status == "Approved":
			frappe.db.set_value(
				"Engineering Project",
				self.engineering_project,
				"project_status",
				"Approved"
			)
