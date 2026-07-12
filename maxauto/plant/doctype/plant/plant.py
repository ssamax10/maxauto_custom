# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe import _
from frappe.model.document import Document


class Plant(Document):
	"""Plant - Manufacturing facility/unit master
	
	Represents a physical manufacturing plant or business unit with:
	- Default warehouses for RM, INQA, and FG
	- Default cost center for accounting
	- Contact information for key departments
	"""
	
	def validate(self):
		"""Validate plant data"""
		self.validate_plant_code()
		self.validate_email()
		self.validate_warehouses()
	
	def validate_plant_code(self):
		"""Ensure plant code follows naming convention"""
		if self.plant_code and not self.plant_code.isupper():
			self.plant_code = self.plant_code.upper()
	
	def validate_email(self):
		"""Validate email format if provided"""
		if self.email and not frappe.utils.validate_email_address(self.email):
			frappe.throw(_("Invalid email address: {0}").format(self.email))
	
	def validate_warehouses(self):
		"""Ensure warehouses are not duplicated"""
		warehouses = [
			self.default_rm_warehouse,
			self.default_inqa_warehouse,
			self.default_fg_warehouse
		]
		# Filter out None values
		warehouses = [w for w in warehouses if w]
		if len(warehouses) != len(set(warehouses)):
			frappe.throw(_("Default warehouses must be unique"))
	
	def before_save(self):
		"""Set defaults before saving"""
		if not self.plant_code:
			frappe.throw(_("Plant Code is required"))
	
	@staticmethod
	def get_active_plants():
		"""Get list of active plants"""
		return frappe.get_all(
			"Plant",
			filters={"is_active": 1},
			fields=["name", "plant_code", "plant_name", "business_unit"],
			order_by="plant_code"
		)
	
	@staticmethod
	def get_plant_warehouses(plant_code):
		"""Get warehouse configuration for a plant"""
		plant = frappe.get_doc("Plant", plant_code)
		return {
			"rm_warehouse": plant.default_rm_warehouse,
			"inqa_warehouse": plant.default_inqa_warehouse,
			"fg_warehouse": plant.default_fg_warehouse,
		}