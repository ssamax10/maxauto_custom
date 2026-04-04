# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class Machine(Document):
	"""Machine master - tracks all production equipment"""
	
	def validate(self):
		"""Validate machine details"""
		if self.spindle_rpm and self.spindle_rpm <= 0:
			frappe.throw("Spindle RPM must be greater than 0")
	
	def on_submit(self):
		"""Actions when machine is submitted"""
		pass
