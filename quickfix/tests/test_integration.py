import frappe
from frappe.tests.utils import FrappeTestCase


class TestIntegration(FrappeTestCase):
	def test_job_card_creates_invoice(self):
		doc = frappe.get_doc(
			{
				"doctype": "Job Card",
				"customer_name": "kumar",
				"customer_phone": "9999999998",
				"device_type": "SmartPhone",
				"problem_description": "Charging Problem",
				"assigned_technician": "TECH-0001",
				"status": "For Delivery",
			}
		)
		doc.insert()
		doc.submit()
		invoices = frappe.get_all("Service Invoice", filters={"job_card": doc.name})

		self.assertGreater(len(invoices), 0)
