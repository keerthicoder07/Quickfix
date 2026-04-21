import re

import frappe


def get_context(context):
	phone = frappe.form_dict.get("phone")

	context.jobs = []

	if phone and len(phone) == 10:
		context.jobs = frappe.get_all(
			"Job Card", filters={"customer_phone": phone}, fields=["name", "status"]
		)

	return context
