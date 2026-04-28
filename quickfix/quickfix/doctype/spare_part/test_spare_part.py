# Copyright (c) 2026, Aerele and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestSparePart(FrappeTestCase):
	def test_part_price_fail(self):
		part = frappe.get_doc(
			{"doctype": "Spare Part", "part_name": "Battery", "unit_cost": 100, "selling_price": 100}
		)

		with self.assertRaises(frappe.ValidationError):
			part.insert()

	def test_part_price_pass(self):
		part = part = frappe.get_doc(
			{"doctype": "Spare Part", "part_name": "Battery", "unit_cost": 100, "selling_price": 101}
		)
		part.insert()
		self.assertGreater(part.selling_price, part.unit_cost)
