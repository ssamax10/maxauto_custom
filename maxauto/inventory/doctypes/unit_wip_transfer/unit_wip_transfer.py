# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.model.document import Document


class UnitWIPTransfer(Document):
	"""Unit WIP Transfer - manages multi-unit manufacturing transfers"""
	
	def validate(self):
		"""Validate transfer"""
		if self.qty <= 0:
			frappe.throw("Quantity must be greater than 0")
		
		if self.source_warehouse == self.target_warehouse:
			frappe.throw("Source and target warehouses must be different")
	
	def on_submit(self):
		"""Create Stock Entry on submission"""
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.doctype_name = "Stock Entry"
		stock_entry.stock_entry_type = "Material Transfer"
		stock_entry.from_warehouse = self.source_warehouse
		stock_entry.to_warehouse = self.target_warehouse
		
		stock_entry.append("items", {
			"item_code": self.item,
			"qty": self.qty,
			"uom": "Kg"
		})
		stock_entry.save()
