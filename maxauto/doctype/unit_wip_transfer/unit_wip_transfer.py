# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe import _
from frappe.model.document import Document


class UnitWIPTransfer(Document):
	"""Unit WIP Transfer - manages multi-unit manufacturing transfers

	Creates a Material Transfer Stock Entry on submit and cancels it on cancel.
	"""

	def validate(self):
		"""Validate transfer"""
		if not self.qty or self.qty <= 0:
			frappe.throw(_("Quantity must be greater than 0"))

		if self.source_warehouse == self.target_warehouse:
			frappe.throw(_("Source and target warehouses must be different"))

		if not self.transfer_date:
			self.transfer_date = frappe.utils.today()

	def on_submit(self):
		"""Create and submit Stock Entry on submission"""
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.stock_entry_type = "Material Transfer"
		stock_entry.purpose = "Material Transfer"
		stock_entry.from_warehouse = self.source_warehouse
		stock_entry.to_warehouse = self.target_warehouse

		# Get item's stock UOM if available, otherwise default to Kg
		item_uom = frappe.db.get_value("Item", self.item, "stock_uom") or "Kg"

		stock_entry.append("items", {
			"item_code": self.item,
			"qty": self.qty,
			"uom": item_uom,
			"transfer_qty": self.qty,
			"s_warehouse": self.source_warehouse,
			"t_warehouse": self.target_warehouse,
		})

		stock_entry.insert()
		stock_entry.submit()

		# Store reference to stock entry on this document
		self.db_set("stock_entry", stock_entry.name)

		frappe.msgprint(
			_("Stock Entry {0} created successfully").format(
				frappe.utils.get_link_to_form("Stock Entry", stock_entry.name)
			),
			alert=True
		)

	def on_cancel(self):
		"""Cancel associated Stock Entry when transfer is cancelled"""
		if not self.stock_entry:
			return

		se_doc = frappe.get_doc("Stock Entry", self.stock_entry)
		if se_doc.docstatus == 1:
			se_doc.cancel()
			frappe.msgprint(
				_("Stock Entry {0} cancelled").format(
					frappe.utils.get_link_to_form("Stock Entry", self.stock_entry)
				),
				alert=True,
				indicator="orange"
			)