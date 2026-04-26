import frappe
from frappe.tests.utils import FrappeTestCase


class TestAPI(FrappeTestCase):
	def test_get_shop_name(self):
		frappe.db.get_single_value("Quickfix Settings", "shop_name", "Power house")
		result = frappe.call("quickfix.api.get_shop_name")

		self.assertEqual(result, "Powerhouse")
