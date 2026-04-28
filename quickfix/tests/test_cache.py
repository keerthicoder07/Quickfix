import frappe
from frappe.tests.utils import FrappeTestCase


class TestCache(FrappeTestCase):
	def test_cache_set_get(self):
		frappe.cache().delete_value("quickfix_test")
		frappe.cache().set_value("quickfix_test", "value")
		val = frappe.cache().get_value("quickfix_test")
		self.assertEqual(val, "value")
