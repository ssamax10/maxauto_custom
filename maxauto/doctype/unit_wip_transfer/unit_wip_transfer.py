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
		"""Create and submit Stock Entry on submission"""
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.stock_entry_type = "Material Transfer"
		stock_entry.from_warehouse = self.source_warehouse
		stock_entry.to_warehouse = self.target_warehouse
		stock_entry.purpose = "Material Transfer"
		
		# Get item's stock UOM if available, otherwise default to Kg
		item_uom = frappe.db.get_value("Item", self.item, "stock_uom") or "Kg"
		
		stock_entry.append("items", {
			"item_code": self.item,
			"qty": self.qty,
			"uom": item_uom,
			"transfer_qty": self.qty
		})
		
		stock_entry.insert()
		stock_entry.submit()
		
		# Store reference to stock entry for tracking
		frappe.db.set_value(self.doctype, self.name, "stock_entry", stock_entry.name)
		
		frappe.msgprint(
			frappe._("Stock Entry {0} created successfully").format(
				frappe.utils.get_link_to_form("Stock Entry", stock_entry.name)
			),
			alert=True
		)
