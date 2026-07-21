# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe import _
from frappe.model.document import Document


class MaterialSpecification(Document):
	"""Material Specification - Technical specifications for raw materials
	
	Tracks:
	- Material properties (type, grade, standard)
	- Mechanical properties (density, tensile/yield strength)
	- Dimensions (diameter, thickness, width, length)
	- Chemical composition (C, Mn, Si, P, S, etc.)
	- Certification requirements
	"""
	
	def validate(self):
		"""Validate material specification"""
		self.validate_material_code()
		self.validate_dimensions()
		self.validate_chemical_composition()
	
	def validate_material_code(self):
		"""Ensure material code is uppercase"""
		if self.material_code and not self.material_code.isupper():
			self.material_code = self.material_code.upper()
	
	def validate_dimensions(self):
		"""Validate dimensional values are positive"""
		dimension_fields = [
			"diameter_mm", "thickness_mm", "width_mm", "length_mm"
		]
		for field in dimension_fields:
			value = getattr(self, field, None)
			if value is not None and value < 0:
				frappe.throw(_("{0} cannot be negative").format(
					self.meta.get_label(field)
				))
	
	def validate_chemical_composition(self):
		"""Validate chemical composition percentages"""
		composition_fields = [
			"carbon", "manganese", "silicon", "phosphorus", "sulfur"
		]
		for field in composition_fields:
			value = getattr(self, field, None)
			if value is not None:
				if value < 0 or value > 100:
					frappe.throw(_("{0} must be between 0 and 100%").format(
						self.meta.get_label(field)
					))
	
	@staticmethod
	def get_specifications_for_item(item_code):
		"""Get all active specifications for an item"""
		return frappe.get_all(
			"Material Specification",
			filters={
				"item": item_code,
				"is_active": 1
			},
			fields=["name", "material_code", "material_name", "material_type", "grade"],
			order_by="material_code"
		)
	
	@staticmethod
	def get_materials_by_type(material_type):
		"""Get all active materials of a specific type"""
		return frappe.get_all(
			"Material Specification",
			filters={
				"material_type": material_type,
				"is_active": 1
			},
			fields=["name", "material_code", "material_name", "grade", "standard"],
			order_by="material_code"
		)