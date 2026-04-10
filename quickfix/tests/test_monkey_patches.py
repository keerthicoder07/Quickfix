import frappe
from frappe.tests.utils import FrappeTestCase


class TestGetUrl(FrappeTestCase):
	def setUp(self):
		from quickfix.quickfix.monkey_patches import apply_all

		apply_all()

	def test_with_prefix(self):
		frappe.conf.custom_url_prefix = "https://cdn.example.com"

		import frappe.utils as fu

		url = fu.get_url("/test")

		self.assertTrue(url.startswith("https://cdn.example.com"))

	def test_without_prefix(self):
		frappe.conf.custom_url_prefix = ""

		import frappe.utils as fu

		url = fu.get_url("/test")

		self.assertFalse(url.startswith("https://cdn.example.com"))
