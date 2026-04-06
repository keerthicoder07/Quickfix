# Copyright (c) 2026, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceInvoice(Document):
	def has_permission(doc, user=None):
		if not user:
			user = frappe.session.user
		roles = frappe.get_roles(user)
		if "QF Manager" in roles:
			return True
		if doc.job_card:
			payment_status = frappe.db.get_value("Job Card", doc.job_card, "payment_status")
			if payment_status != "Paid":
				return False
		return True
