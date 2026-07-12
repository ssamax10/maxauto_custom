# Copyright (c) 2025, Max Auto Cables Pvt Ltd
# License: MIT

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPlant(FrappeTestCase):
	"""Test cases for Plant DocType"""
	
	def setUp(self):
		"""Create test plant"""
		if frappe.db.exists("Plant", "TEST-001"):
			frappe.delete_doc("Plant", "TEST-001", force=True)
		
		self.plant = frappe.get_doc({
			"doctype": "Plant",
			"plant_code": "TEST-001",
			"plant_name": "Test Plant",
			"business_unit": "TEST-BU",
			"is_active": 1,
			"email": "test@maxautocables.com"
		})
	
	def tearDown(self):
		"""Clean up test data"""
		if frappe.db.exists("Plant", "TEST-001"):
			frappe.delete_doc("Plant", "TEST-001", force=True)
	
	def test_plant_creation(self):
		"""Test that plant can be created"""
		self.plant.insert()
		self.assertTrue(frappe.db.exists("Plant", "TEST-001"))
	
	def test_plant_code_uppercase(self):
		"""Test that plant code is converted to uppercase"""
		self.plant.plant_code = "test-001"
		self.plant.insert()
		self.assertEqual(self.plant.plant_code, "TEST-001")
	
	def test_invalid_email(self):
		"""Test that invalid email raises error"""
		self.plant.email = "invalid-email"
		with self.assertRaises(frappe.ValidationError):
			self.plant.insert()
	
	def test_unique_warehouses(self):
		"""Test that warehouses must be unique"""
		self.plant.default_rm_warehouse = "Stores - TC"
		self.plant.default_fg_warehouse = "Stores - TC"  # Same warehouse
		with self.assertRaises(frappe.ValidationError):
			self.plant.insert()
	
	def test_get_active_plants(self):
		"""Test get_active_plants static method"""
		from maxauto_custom.maxauto.plant.doctype.plant.plant import Plant
		
		self.plant.insert()
		active_plants = Plant.get_active_plants()
		plant_codes = [p.plant_code for p in active_plants]
		self.assertIn("TEST-001", plant_codes)