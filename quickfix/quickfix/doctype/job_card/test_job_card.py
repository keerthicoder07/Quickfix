# Copyright (c) 2026, Aerele and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestJobCard(FrappeTestCase):
	def create_job_card(self):
		doc = frappe.get_doc(
			{
				"doctype": "Job Card",
				"customer_name": "kumar",
				"customer_phone": "9999999999",
				"device_type": "SmartPhone",
				"problem_description": "Charging Problem",
				"assigned_technician": "TECH-0001",
			}
		)
		doc.insert()
		return doc

	def test_job_card_creation(self):
		doc = self.create_job_card()

		self.assertIsNotNone(doc.name)
		self.assertEqual(doc.status, "Draft")

	def test_status_update(self):
		doc = self.create_job_card()

		doc.status = "Delivered"
		doc.save()

		updated = frappe.get_doc("Job Card", doc.name)

		self.assertEqual(updated.status, "Delivered")

	def test_invalid_phone(self):
		doc = frappe.get_doc(
			{
				"doctype": "Job Card",
				"customer_name": "kumar",
				"customer_phone": "123",
				"device_type": "SmartPhone",
				"problem_description": "Charging Problem",
				"assigned_technician": "TECH-0001",
			}
		)

		with self.assertRaises(Exception):
			doc.insert()

	def test_final_amount_computation(self):
		doc = self.create_job_card()
		expected_parts_total = 0
		expected_labour = 500
		self.assertEqual(doc.parts_total, expected_parts_total)
		self.assertEqual(doc.final_amount, expected_parts_total + expected_labour)
