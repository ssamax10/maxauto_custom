# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT
# See license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class EngineeringProject(Document):
	"""Engineering Project DocType for managing CNC and rope/cable projects"""

	def before_insert(self):
		"""Set created date on insert (project_id is auto-named via autoname)"""
		if not self.created_date:
			self.created_date = frappe.utils.today()

	def validate(self):
		"""Validate Engineering Project fields"""
		if self.project_status == "Completed" and not self.specifications:
			frappe.throw(_("Cannot mark project as Completed without specifications"))

	def before_save(self):
		"""Set project_id from name and update modified date on every save"""
		if not self.project_id:
			self.project_id = self.name
		self.modified_date = frappe.utils.today()

	def on_submit(self):
		"""Record submission timestamp"""
		self.db_set("modified_date", frappe.utils.today())

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