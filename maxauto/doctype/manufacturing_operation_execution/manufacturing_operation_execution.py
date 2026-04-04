# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document
from datetime import datetime


class ManufacturingOperationExecution(Document):
	"""MES - Manufacturing Operation Execution tracking"""
	
	def validate(self):
		"""Validate execution data"""
		if not self.start_time:
			self.start_time = frappe.utils.now_datetime()
		
		if self.end_time and self.start_time:
			duration = (self.end_time - self.start_time).total_seconds() / 60
			if duration < 0:
				frappe.throw("End time must be after start time")
		
		if self.actual_qty < 0:
			frappe.throw("Actual quantity cannot be negative")
		
		if self.rejected_qty < 0:
			frappe.throw("Rejected quantity cannot be negative")
	
	def on_submit(self):
		"""Log operation completion"""
		# Create MES event log
		event_log = frappe.new_doc("MES Event Log")
		event_log.event_type = "Operation Complete"
		event_log.manufacturing_operation_execution = self.name
		event_log.machine = self.machine
		event_log.operator = self.operator
		event_log.qty_produced = self.actual_qty
		event_log.qty_rejected = self.rejected_qty
		event_log.save()
