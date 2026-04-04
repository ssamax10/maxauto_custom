# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT
# See license.txt

import frappe
from frappe.model.document import Document


class EngineeringProject(Document):
	"""Engineering Project DocType for managing CNC and rope/cable projects"""
	
	def before_insert(self):
		# Auto-generate project_id if not already set
		if not self.project_id:
			last_project = frappe.db.get_value(
				"Engineering Project",
				{},
				"project_id",
				order_by="name desc",
				limit=1
			)
			if last_project:
				# Extract number and increment
				pass
			self.project_id = self.name
	
	def validate(self):
		"""Validate Engineering Project fields"""
		if self.project_status == "Completed" and not self.specifications:
			frappe.throw("Cannot mark project as Completed without specifications")
	
	def on_submit(self):
		"""Record submission timestamp"""
		frappe.db.set_value(self.doctype, self.name, "modified_date", frappe.utils.today())
	
	def get_linked_sales_orders(self):
		"""Get all linked sales orders"""
		return frappe.get_all(
			"Sales Order",
			filters={"engineering_project": self.name},
			fields=["name", "customer", "total"]
		)
	
	def get_linked_work_orders(self):
		"""Get all linked work orders"""
		return frappe.get_all(
			"Work Order",
			filters={"engineering_project": self.name},
			fields=["name", "item_code", "qty"]
		)
