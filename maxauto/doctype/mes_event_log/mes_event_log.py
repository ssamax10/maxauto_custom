# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class MESEventLog(Document):
	"""MES Event Log - logs all shop floor events from Qcadoo"""
	
	def validate(self):
		"""Validate event log"""
		if not self.event_timestamp:
			self.event_timestamp = frappe.utils.now_datetime()
