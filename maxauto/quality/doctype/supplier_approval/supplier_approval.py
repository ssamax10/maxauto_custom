# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today, getdate


class SupplierApproval(Document):
	"""Supplier Approval - Quality approval workflow for suppliers
	
	Tracks:
	- Supplier approval status (Pending, Approved, Conditionally Approved, Rejected, Expired)
	- ISO certification details
	- Audit information and scores
	- Quality agreements and requirements
	- Approved materials list
	"""
	
	def validate(self):
		"""Validate supplier approval"""
		self.validate_email()
		self.validate_dates()
		self.validate_approval_status()
	
	def validate_email(self):
		"""Validate email format if provided"""
		if self.email and not frappe.utils.validate_email_address(self.email):
			frappe.throw(_("Invalid email address: {0}").format(self.email))
	
	def validate_dates(self):
		"""Validate date fields"""
		if self.certificate_valid_until and self.approval_date:
			if getdate(self.certificate_valid_until) < getdate(self.approval_date):
				frappe.throw(_("Certificate valid until date cannot be before approval date"))
		
		if self.next_audit_date and self.last_audit_date:
			if getdate(self.next_audit_date) <= getdate(self.last_audit_date):
				frappe.throw(_("Next audit date must be after last audit date"))
	
	def validate_approval_status(self):
		"""Validate approval status transitions"""
		if self.approval_status == "Approved" and not self.approval_date:
			self.approval_date = today()
		
		if self.approval_status == "Approved" and not self.approved_by:
			self.approved_by = frappe.session.user
	
	def on_submit(self):
		"""Actions on submission"""
		if self.approval_status == "Approved":
			frappe.msgprint(
				_("Supplier {0} has been approved").format(self.supplier_name),
				alert=True
			)
		elif self.approval_status == "Rejected":
			frappe.msgprint(
				_("Supplier {0} approval has been rejected").format(self.supplier_name),
				alert=True,
				indicator="red"
			)
	
	def on_cancel(self):
		"""Actions on cancellation"""
		frappe.msgprint(
			_("Supplier Approval for {0} has been cancelled").format(self.supplier_name),
			alert=True,
			indicator="orange"
		)
	
	@staticmethod
	def get_approved_suppliers():
		"""Get list of approved suppliers"""
		return frappe.get_all(
			"Supplier Approval",
			filters={
				"approval_status": "Approved",
				"docstatus": 1
			},
			fields=["name", "supplier", "supplier_name", "supplier_type"],
			order_by="supplier_name"
		)
	
	@staticmethod
	def is_supplier_approved(supplier):
		"""Check if a supplier is approved"""
		return frappe.db.exists(
			"Supplier Approval",
			{
				"supplier": supplier,
				"approval_status": "Approved",
				"docstatus": 1
			}
		)
	
	@staticmethod
	def get_suppliers_needing_audit():
		"""Get suppliers whose audit is due or overdue"""
		return frappe.get_all(
			"Supplier Approval",
			filters={
				"approval_status": "Approved",
				"docstatus": 1,
				"next_audit_date": ("<=", today())
			},
			fields=["name", "supplier", "supplier_name", "last_audit_date", "next_audit_date"],
			order_by="next_audit_date"
		)