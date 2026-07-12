# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe import _
from frappe.model.document import Document


class PackingRecord(Document):
	"""Packing Record - Tracks finished goods packing operations
	
	Captures:
	- Packing details (quantity, weight, container/drum)
	- Quality status
	- Creates stock entry to move packed goods to FG warehouse
	"""
	
	def validate(self):
		"""Validate packing record"""
		if self.quantity <= 0:
			frappe.throw(_("Quantity must be greater than 0"))
		
		if self.total_weight_kg and self.total_weight_kg <= 0:
			frappe.throw(_("Total weight must be greater than 0"))
		
		if self.net_weight_kg and self.net_weight_kg < 0:
			frappe.throw(_("Net weight cannot be negative"))
		
		if self.gross_weight_kg and self.gross_weight_kg < 0:
			frappe.throw(_("Gross weight cannot be negative"))
	
	def on_submit(self):
		"""Create stock entry to move packed goods to FG warehouse"""
		if not self.item:
			frappe.throw(_("Item is required to create stock entry"))
		
		# Only create stock entry if source and target warehouses are set
		if not self.source_warehouse or not self.target_warehouse:
			frappe.msgprint(
				_("Source and target warehouses not set. Stock entry not created."),
				alert=True,
				indicator="yellow"
			)
			return
		
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.stock_entry_type = "Material Transfer"
		stock_entry.purpose = "Material Transfer"
		stock_entry.from_warehouse = self.source_warehouse
		stock_entry.to_warehouse = self.target_warehouse
		
		# Get item's stock UOM if available, otherwise default to Kg
		item_uom = frappe.db.get_value("Item", self.item, "stock_uom") or "Kg"
		
		# Use total weight if available, otherwise use quantity
		transfer_qty = self.total_weight_kg or self.quantity
		
		stock_entry.append("items", {
			"item_code": self.item,
			"qty": transfer_qty,
			"uom": item_uom,
			"transfer_qty": transfer_qty,
			"s_warehouse": self.source_warehouse,
			"t_warehouse": self.target_warehouse
		})
		
		stock_entry.insert()
		stock_entry.submit()
		
		# Store reference to stock entry for tracking
		frappe.db.set_value(self.doctype, self.name, "stock_entry", stock_entry.name)
		
		frappe.msgprint(
			_("Stock Entry {0} created for packed goods").format(
				frappe.utils.get_link_to_form("Stock Entry", stock_entry.name)
			),
			alert=True
		)
	
	def on_cancel(self):
		"""Cancel associated stock entry when packing record is cancelled"""
		stock_entry = frappe.db.get_value(self.doctype, self.name, "stock_entry")
		if stock_entry:
			se_doc = frappe.get_doc("Stock Entry", stock_entry)
			if se_doc.docstatus == 1:
				se_doc.cancel()
				frappe.msgprint(
					_("Stock Entry {0} cancelled").format(
						frappe.utils.get_link_to_form("Stock Entry", stock_entry)
					),
					alert=True
				)
